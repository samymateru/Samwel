import os
import json
import asyncio
from aio_pika import connect_robust, ExchangeType, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from dotenv import load_dotenv

load_dotenv()

class RabbitMQ:
    """Singleton RabbitMQ connection manager."""
    _instance = None

    def __init__(self):
        self._connection: AbstractRobustConnection | None = None
        self._channels: set[AbstractRobustChannel] = set()
        self._lock = asyncio.Lock()

        self.amqp_url = os.getenv(
            "AMQP_URL",
            f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@"
            f"{os.getenv('RABBITMQ_HOST')}:{os.getenv('RABBITMQ_PORT')}/"
        )

    @classmethod
    def instance(cls) -> "RabbitMQ":
        if cls._instance is None:
            cls._instance = RabbitMQ()
        return cls._instance

    async def get_connection(self) -> AbstractRobustConnection:
        if self._connection is None or self._connection.is_closed:
            self._connection = await connect_robust(self.amqp_url)
        return self._connection

    async def get_channel(self) -> AbstractRobustChannel:
        async with self._lock:
            connection = await self.get_connection()
            channel = await connection.channel()
            self._channels.add(channel)
            return channel

    async def close(self):
        for ch in self._channels:
            if not ch.is_closed:
                await ch.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()



# --- Publisher helper ---
async def publish(queue_name: str, payload: dict, exchange_name: str = "my_exchange"):
    rmq = RabbitMQ.instance()
    channel = await rmq.get_channel()
    exchange = await channel.declare_exchange(exchange_name, ExchangeType.DIRECT, durable=True)
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange, routing_key=queue_name)

    await exchange.publish(
        Message(body=json.dumps(payload).encode(), content_type="application/json"),
        routing_key=queue_name
    )
    await channel.close()
