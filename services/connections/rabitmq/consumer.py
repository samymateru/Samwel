import asyncio
import json
from aio_pika import ExchangeType, IncomingMessage

from services.connections.rabitmq.rabbitmq import RabbitMQ
from services.notifications.postmark import email_service
from services.logging.logger import global_logger

async def message_handler(message: IncomingMessage):
    async with message.process():
        queue_name = message.routing_key
        try:
            data = json.loads(message.body.decode())
        except json.JSONDecodeError:
            data = {"mode": "single", "data": {}}


        if queue_name == "users" and data.get("mode") == "single":
            await email_service.send_with_template(data["data"])
            global_logger.info(f"Mail sent successfully")
        elif queue_name == "issue" and data.get("mode") == "single":
            await email_service.send_issue_notification(data["data"])
            global_logger.info("Issue notification sent")
        elif queue_name == "sam":
            # Handle messages from the "sam" queue
            global_logger.info(f"Processed message from 'sam': {data}")


async def start_consumer():
    rmq = RabbitMQ.instance()
    channel = await rmq.get_channel()
    exchange_name = "my_exchange"
    exchange = await channel.declare_exchange(exchange_name, ExchangeType.DIRECT, durable=True)

    queues = ["issue", "users", "sam"]
    for q_name in queues:
        queue = await channel.declare_queue(q_name, durable=True)
        await queue.bind(exchange, routing_key=q_name)
        await queue.consume(message_handler)

    print(f"[*] Waiting for messages on queues: {queues}")
    await asyncio.Future()  # run forever
