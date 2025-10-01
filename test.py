import asyncio
import aio_pika

async def main():
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust(
        "amqp://myuser:mypassword@<SERVER_IP>:5672/"
    )


    async with connection:
        # Create a channel
        channel = await connection.channel()

        # Declare a queue
        queue = await channel.declare_queue("test_queue", durable=True)

        # Publish a message
        await channel.default_exchange.publish(
            aio_pika.Message(body=b"Hello, RabbitMQ!"),
            routing_key=queue.name,
        )

        print("Message sent!")

        # Consume messages
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print("Received message:", message.body.decode())
                    break  # stop after first message for demo

asyncio.run(main())
