import os
import json
import pika
from threading import Lock
from dotenv import load_dotenv

load_dotenv()


class RabbitMQ:
    """Singleton RabbitMQ connection manager using pika (synchronous)."""

    _instance = None
    _lock = Lock()

    def __init__(self):
        self._connection = None
        self._channel = None

        self.exchange_name = "my_exchange"
        self.connection_params = pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            port=int(os.getenv("RABBITMQ_PORT", 5672)),
            heartbeat=600,
            blocked_connection_timeout=300,
        )

    @classmethod
    def instance(cls):
        """Thread-safe singleton instance."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = RabbitMQ()
        return cls._instance

    def _ensure_connection(self):
        """Ensure there is a valid open connection and channel."""
        if self._connection is None or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self.connection_params)
            self._channel = self._connection.channel()

            # Ensure the exchange exists
            self._channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type="direct",
                durable=True
            )

        elif self._channel is None or self._channel.is_closed:
            self._channel = self._connection.channel()

    def publish(self, queue_name: str, payload: dict):
        """Publish a JSON message to a queue via exchange."""
        self._ensure_connection()

        # Ensure queue exists and is bound
        self._channel.queue_declare(queue=queue_name, durable=True)
        self._channel.queue_bind(
            exchange=self.exchange_name,
            queue=queue_name,
            routing_key=queue_name
        )

        # Convert payload to JSON safely (handling datetimes)
        body = json.dumps(payload, default=str).encode()

        # Publish the message
        self._channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=queue_name,
            body=body,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # persistent message
            ),
        )

        print(f"[>] Sent to '{queue_name}': {payload}")

    def close(self):
        """Close channel and connection gracefully."""
        try:
            if self._channel and self._channel.is_open:
                self._channel.close()
            if self._connection and self._connection.is_open:
                self._connection.close()
        except Exception:
            pass
