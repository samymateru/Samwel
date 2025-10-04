import json
import os
import asyncio
import sys
import threading
import logging
from dotenv import load_dotenv
from aio_pika import connect_robust, IncomingMessage, Message, ExchangeType

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

    async def _setup_exchange(self):
        """Helper to declare exchange and channel if not already created."""
        if not self._connection:
            self._connection = await connect_robust(self.amqp_url)
        if not self._channel:
            self._channel = await self._connection.channel()
        if not self._exchange:
            self._exchange = await self._channel.declare_exchange(
                self.exchange_name, ExchangeType.DIRECT, durable=True
            )

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

        finally:
            await self._close()

    async def _process_message(self, message: IncomingMessage, queue_name: str):
        """Process incoming messages."""
        async with message.process():
            body = message.body.decode()

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {"mode": 'single', "data": ""}


            if queue_name == "user":
                if data["mode"] == "single":
                    await email_service.send_with_template(data["data"])


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

        # Only run cleanup if the loop is still alive
        if self.loop.is_running() and not self.loop.is_closed():
            try:
                # Schedule coroutine cleanup safely
                asyncio.run_coroutine_threadsafe(self._close(), self.loop)

                # Stop loop safely
                self.loop.call_soon_threadsafe(self.loop.stop)
            except RuntimeError as e:
                # Loop may already be closed, ignore gracefully
                print(f"Loop already closed: {e}")


consumer = RabbitMQMultiQueue(["user", "issue", "queue_3"])
consumer.start()
