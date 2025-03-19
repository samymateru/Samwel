import pika
import os

import json

RABBITMQ_URL = os.getenv("localhost", "amqp://guest:guest@localhost:5672/")


class RabbitMQConnection:
    """Manages RabbitMQ connection and channel."""
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self, queue_name: str):
        """Establish RabbitMQ connection and declare queue."""
        if not self.connection or self.connection.is_closed:
            params = pika.URLParameters(RABBITMQ_URL)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue_name, durable=True)
            print("✅ RabbitMQ connected!")

    def publish_message(self, message: dict, queue_name: str):
        """Publish a message to RabbitMQ."""
        try:
            if not self.channel or self.channel.is_closed:
                self.connect(queue_name="task")

            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                ),
            )
            print(f"Produced: {message}")
        except Exception as e:
            print(e)

    def consume_messages(self, queue_name: str):

        def callback(ch, method, properties, body):
            print(f"Received message: {body.decode()}")
            # Process your message here

        if not self.channel or self.channel.is_closed:
            self.connect(queue_name="task")
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print("Started consuming messages...")
        self.channel.start_consuming()

    def close(self):
        """Close the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("❌ RabbitMQ connection closed!")

rabbitmq = RabbitMQConnection()