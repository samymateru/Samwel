import os
from typing import Optional
import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from dotenv import load_dotenv

load_dotenv()


class AsyncRabbitMQSingleton:
    """
    Singleton class for managing a single aio-pika RabbitMQ connection.

    - Ensures only one RabbitMQ connection is created and reused.
    - Provides channels from the shared connection.
    - Handles graceful shutdown and cleanup.
    """

    _instance = None

    def __init__(self):
        self._connection: Optional[AbstractRobustConnection] = None

    @classmethod
    def get_instance(cls) -> "AsyncRabbitMQSingleton":
        if cls._instance is None:
            cls._instance = AsyncRabbitMQSingleton()
        return cls._instance

    async def get_connection(self) -> AbstractRobustConnection:
        """
        Get or create the RabbitMQ connection.
        Uses environment variables for configuration.
        """
        if self._connection is None or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(
                url=(
                    f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}"
                    f"@{os.getenv('RABBITMQ_HOST')}:{os.getenv('RABBITMQ_PORT')}/"
                ),
                client_properties={"connection_name": "fastapi-app"},
            )
        return self._connection

    async def get_channel(self) -> AbstractRobustChannel:
        """
        Open a new channel from the RabbitMQ connection.
        """
        connection = await self.get_connection()
        channel = await connection.channel()
        return channel

    async def close_connection(self):
        """
        Close the RabbitMQ connection if it exists.
        """
        if self._connection and not self._connection.is_closed:
            await self._connection.close()


# Dependency for FastAPI
async def get_rabbitmq_channel():
    """
    Dependency to be used inside FastAPI endpoints
    for getting a fresh channel.
    """
    channel = await AsyncRabbitMQSingleton.get_instance().get_channel()
    try:
        yield channel
    finally:
        # Closing channel after request prevents resource leaks
        if not channel.is_closed:
            await channel.close()
