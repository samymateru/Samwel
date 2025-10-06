import json
import os
import sys
import asyncio
import threading
import logging

import aio_pika
from aio_pika import connect_robust, Message, ExchangeType, IncomingMessage
from dotenv import load_dotenv

from services.logging.logger import global_logger
from services.notifications.postmark import email_service

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RabbitMQMultiQueue(threading.Thread):
    def __init__(self, queues: list[str], exchange_name: str = "my_exchange"):
        super().__init__(daemon=True)
        self.queues = queues
        self.exchange_name = exchange_name
        self.amqp_url = os.getenv(
            "AMQP_URL",
            f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@"
            f"{os.getenv('RABBITMQ_HOST')}:{os.getenv('RABBITMQ_PORT')}/"
        )
        self.loop: asyncio.AbstractEventLoop | None = None
        self._stop_event = threading.Event()
        self._ready_event = threading.Event()
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.Channel | None = None
        self._exchange: aio_pika.Exchange | None = None
        self._publish_queue: asyncio.Queue = asyncio.Queue()

    def run(self):
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self._consume())
        except Exception as e:
            logger.exception(f"RabbitMQ loop crashed: {e}")
        finally:
            if not self.loop.is_closed():
                self.loop.close()

    async def _setup_exchange(self):
        self._connection = await aio_pika.connect_robust(self.amqp_url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name, ExchangeType.DIRECT, durable=True
        )

        # Bind queues and register consumers
        for queue_name in self.queues:
            queue = await self._channel.declare_queue(queue_name, durable=True)
            await queue.bind(self._exchange, routing_key=queue_name)

            async def callback(message: IncomingMessage, qname=queue_name):
                await self._process_message(message, qname)

            await queue.consume(callback)

        logger.info("✅ RabbitMQ consumer fully ready.")
        self._ready_event.set()

    async def _publisher_task(self):
        while not self._stop_event.is_set():
            queue_name, body = await self._publish_queue.get()
            try:
                await self._exchange.publish(
                    Message(body=json.dumps(body).encode(), content_type="application/json"),
                    routing_key=queue_name
                )
                logger.info(f"✅ Published message to {queue_name}")
            except Exception as e:
                logger.exception(f"❌ Failed to publish to {queue_name}: {e}")
            finally:
                self._publish_queue.task_done()

    async def _consume(self):
        await self._setup_exchange()
        # Start publisher task **after queues are ready**
        asyncio.create_task(self._publisher_task())
        logger.info(f"🎧 Listening on queues: {', '.join(self.queues)}")

        while not self._stop_event.is_set():
            await asyncio.sleep(1)

    async def _process_message(self, message: IncomingMessage, queue_name: str):
        async with message.process():
            data = json.loads(message.body.decode())
            print(f"📩 Received on '{queue_name}': {data}")
            logger.info(f"📩 Received message on '{queue_name}': {data}")

    def publish(self, queue_name: str, body: dict):
        """
        Thread-safe publisher.
        This ensures the message is immediately picked up by the _publisher_task.
        """
        if not self._ready_event.is_set():
            # Wait for consumer and queues to be fully ready
            self._ready_event.wait()

        # Schedule immediately
        future = asyncio.run_coroutine_threadsafe(
            self._publish_queue.put((queue_name, body)),
            self.loop
        )
        # Wait until the message is actually in the asyncio queue
        future.result()

        logger.info(f"📨 Queued message for {queue_name}")


    def stop(self):
        """Stop consumer and publisher gracefully."""
        self._stop_event.set()
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self._connection.close(), self.loop)
            self.loop.call_soon_threadsafe(self.loop.stop)


# -----------------------------
# Global instance
consumer = RabbitMQMultiQueue(["user", "issue"])
consumer.start()

# Wait until ready before publishing
consumer._ready_event.wait(timeout=10)
logger.info("✅ RabbitMQ Consumer is ready and listening in background")
