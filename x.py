import asyncio
import json
import asyncpg


async def test_function():
    conn = await asyncpg.connect(
        user='postgres', password='25803690Reg', database='EAUDIT', host='eauditrisk.com'
    )

    await conn.add_listener('users_channel', callback)

    print("Listening for user changes...")
    while True:
        await asyncio.sleep(3600)  # keep running



async def callback(connection, pid, channel, payload):
    data = json.loads(payload)
    print("Change detected:", data)


asyncio.run(test_function())