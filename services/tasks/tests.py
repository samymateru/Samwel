import asyncio
from services.tasks.task_schedular import AsyncPersistentQueue


async def main():
    queue = AsyncPersistentQueue("tasks.log")

    # Enqueue tasks
    await queue.enqueue({"task": "send_email", "to": "user@example.com"})
    await queue.enqueue({"task": "generate_report", "user_id": 42})

    print("Queue size after enqueue:", await queue.size())

    # Dequeue tasks
    task1 = await queue.dequeue()
    print("Dequeued:", task1)


    task2 = await queue.dequeue()
    print("Dequeued:", task2)


    task3 = await queue.dequeue()
    print("Dequeued:", task3)


    # After processing
    print("Queue size after processing:", await queue.size())

asyncio.run(main())