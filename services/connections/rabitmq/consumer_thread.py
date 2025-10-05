import json
import os
import asyncio
import sys
import threading
import logging
from dotenv import load_dotenv
from aio_pika import connect_robust, IncomingMessage, Message, ExchangeType
from aio_pika.exceptions import AMQPConnectionError

from services.logging.logger import global_logger
from services.notifications.postmark import email_service

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RabbitMQMultiQueue(threading.Thread):
    def __init__(self, queues: list[str], exchange_name: str = "my_exchange"):
        """
        Multi-queue RabbitMQ consumer and publisher in a background thread.

        Args:
            queues (list[str]): List of queue names to consume.
            exchange_name (str): Exchange to use for publishing messages.
        """
        super().__init__(daemon=True)
        self.queues = queues
        self.exchange_name = exchange_name
        self.amqp_url = os.getenv(
            "AMQP_URL",
            f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@{os.getenv('RABBITMQ_HOST')}:{os.getenv('RABBITMQ_PORT')}/"
        )
        self.loop: asyncio.AbstractEventLoop | None = None
        self._stop_event = threading.Event()
        self._connection = None
        self._channel = None
        self._exchange = None
        self._publish_queue: asyncio.Queue = asyncio.Queue()

    def run(self):
        """Start the async event loop for RabbitMQ consumption and publishing."""
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._consume())


    async def _publisher_task(self):
        """Background async task that publishes messages from the internal queue."""
        while not self._stop_event.is_set():
            queue_name, body = await self._publish_queue.get()
            try:
                if not self._exchange:
                    await self._setup_exchange()
                await self._exchange.publish(
                    Message(
                        body=json.dumps(body).encode(),
                        content_type="application/json"
                    ),
                    routing_key=queue_name
                )
            except Exception as e:
                logger.exception(f"Failed to publish message to {queue_name}: {e}")
            finally:
                self._publish_queue.task_done()


    async def _setup_exchange(self, retries: int = 5, delay: float = 5.0):
        """
        Helper to declare exchange and channel if not already created.
        Retries on connection failure with exponential backoff.
        """
        attempt = 0
        while attempt < retries and not self._stop_event.is_set():
            try:
                if not self._connection or self._connection.is_closed:
                    self._connection = await connect_robust(self.amqp_url)
                if not self._channel or self._channel.is_closed:
                    self._channel = await self._connection.channel()
                if not self._exchange:
                    self._exchange = await self._channel.declare_exchange(
                        self.exchange_name, ExchangeType.DIRECT, durable=True
                    )
                return  # success
            except AMQPConnectionError as e:
                attempt += 1
                logger.warning(f"RabbitMQ connection failed (attempt {attempt}/{retries}): {e}")
                await asyncio.sleep(delay * 2 ** (attempt - 1))  # exponential backoff
            except Exception as e:
                attempt += 1
                logger.exception(f"Unexpected error setting up RabbitMQ (attempt {attempt}/{retries}): {e}")
                await asyncio.sleep(delay * 2 ** (attempt - 1))

        raise ConnectionError(f"Could not connect to RabbitMQ after {retries} attempts")

    def publish(self, queue_name: str, body: dict):
        """Thread-safe publisher for external callers (FastAPI endpoints, etc.)."""
        if not self.loop:
            raise RuntimeError("Consumer loop not running yet!")
        asyncio.run_coroutine_threadsafe(
            self._publish_queue.put((queue_name, body)),
            self.loop
        )


    async def _consume(self):
        """Connect to RabbitMQ, declare queues and exchange, and start consuming."""
        while not self._stop_event.is_set():
            try:
                await self._setup_exchange()

                # Start publisher task
                asyncio.create_task(self._publisher_task())

                # Declare and bind queues
                for q in self.queues:
                    queue = await self._channel.declare_queue(q, durable=True)
                    await queue.bind(self._exchange, routing_key=q)
                    await queue.consume(lambda msg, queue_name=q: self._process_message(msg, queue_name))

                logger.info(f"Listening on queues: {', '.join(self.queues)}")

                # Keep the loop alive
                while not self._stop_event.is_set():
                    await asyncio.sleep(1)

            except Exception as e:
                logger.exception(f"RabbitMQ consumer crashed: {e}")
                await asyncio.sleep(5)  # wait before retrying


    async def _process_message(self, message: IncomingMessage, queue_name: str):
        """Process incoming messages."""
        async with message.process():
            body = message.body.decode()
            global_logger.info("Mail Published On Exchange")

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                global_logger.error("Error parsing message JSON")
                data = {"mode": 'single', "data": ""}

            if queue_name == "user" and data.get("mode") == "single":
                await email_service.send_with_template(data["data"])
                global_logger.info("Mail Sent Successfully")


    async def _close(self):
        """Gracefully close channel and connection."""
        try:
            if self._channel and not self._channel.is_closed:
                await self._channel.close()
            if self._connection and not self._connection.is_closed:
                await self._connection.close()
            logger.info("RabbitMQ connection closed gracefully")
        except Exception as e:
            logger.exception(f"Error closing RabbitMQ connection: {e}")


    def stop(self):
        """Stop consumer and publisher gracefully."""
        self._stop_event.set()

        if not self.loop:
            return

        if self.loop.is_running() and not self.loop.is_closed():
            try:
                asyncio.run_coroutine_threadsafe(self._close(), self.loop)
                self.loop.call_soon_threadsafe(self.loop.stop)
            except RuntimeError as e:
                print(f"Loop already closed: {e}")


# Start consumer
consumer = RabbitMQMultiQueue(["user", "issue", "queue_3"])
consumer.start()
