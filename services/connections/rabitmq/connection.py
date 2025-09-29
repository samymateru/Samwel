import aio_pika
from typing import AsyncGenerator, Optional
from aio_pika.abc import AbstractRobustChannel


class AioPikaConnectionSingleton:
    _instance: Optional["AioPikaConnectionSingleton"] = None


    def __init__(self, amqp_url: str):
        self._amqp_url = amqp_url
        self._connection: Optional[aio_pika.RobustConnection] = None


    @classmethod
    def get_instance(cls, amqp_url: str = "amqp://guest:guest@localhost/") -> "AioPikaConnectionSingleton":
        if cls._instance is None:
            cls._instance = AioPikaConnectionSingleton(amqp_url)
        return cls._instance


    async def connect(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(self._amqp_url)
        return self._connection


    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()


    async def get_channel(self) -> AbstractRobustChannel:
        connection = await self.connect()
        channel = await connection.channel()
        return channel


# Dependency-like async generator to get a channel and close after use if needed:
async def get_rabbitmq_channel() -> AsyncGenerator[aio_pika.RobustChannel, None]:
    singleton = AioPikaConnectionSingleton.get_instance()
    channel = await singleton.get_channel()
    try:
        yield channel
    finally:
        # Optionally: close channel if needed (channels close automatically on connection close)
        await channel.close()
