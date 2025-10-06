import os
import json
import threading
import time
import pika
from dotenv import load_dotenv

from services.logging.logger import global_logger
from services.notifications.postmark import email_service

load_dotenv()


def consume_rabbitmq():
    """Run a blocking RabbitMQ consumer (pika) inside a thread."""

    try:
        connection_params = pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            port=int(os.getenv("RABBITMQ_PORT", 5672)),
            heartbeat=600,
            blocked_connection_timeout=300,
        )

        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        # Declare exchange and queues
        exchange_name = "my_exchange"
        queues = ["issue", "users", "sam"]

        channel.exchange_declare(exchange=exchange_name, exchange_type="direct", durable=True)

        for q in queues:
            channel.queue_declare(queue=q, durable=True)
            channel.queue_bind(exchange=exchange_name, queue=q, routing_key=q)

        channel.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            queue_name = method.routing_key
            try:
                data = json.loads(body.decode())
            except json.JSONDecodeError:
                data = {"mode": "single", "data": {}}


            # handle messages based on queue
            if queue_name == "users" and data.get("mode") == "single":
                email_service.send_with_template(data=data["data"])
                global_logger.info("Mail sent successfully")


            elif queue_name == "issue" and data.get("mode") == "single":
                print("sent to issue")
                email_service.send_issue_notification(data["data"])
                global_logger.info("Issue notification sent")


            elif queue_name == "sam":
                global_logger.info(f"Processed message from 'sam': {data}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Attach callback to all queues
        for q in queues:
            channel.basic_consume(queue=q, on_message_callback=callback, auto_ack=False)

        print(f"[*] Waiting for messages on queues: {queues}")
        channel.start_consuming()

    except Exception as e:
        global_logger.error(f"RabbitMQ consumer error: {e}")
        time.sleep(5)
        consume_rabbitmq()  # auto-restart if crashed


def start_rabbitmq_consumer_thread():
    """Start the RabbitMQ consumer in a background thread."""
    thread = threading.Thread(target=consume_rabbitmq, daemon=True)
    thread.start()
    print("[*] RabbitMQ consumer thread started.")
