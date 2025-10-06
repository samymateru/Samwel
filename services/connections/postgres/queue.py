import asyncio

from psycopg import AsyncConnection


async def listen_notifications(connection: AsyncConnection):
    await connection.execute("LISTEN user_updates;")
    print("Listening on channel 'user_updates'...")

    while True:
        connection.notifies()
        notification = await connection.notifications.get()
        # Example: handle notification
        print(f"Received on {notification.channel}: {notification.payload}")
        # You can trigger async tasks here
        # asyncio.create_task(process_notification(notification.payload))


def notification_handler(conn, pid, channel, payload):
    print(f"Received notification on {channel}: {payload}")
    # Here you can trigger further async tasks