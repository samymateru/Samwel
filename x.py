import asyncio
import os
import sys

from dotenv import load_dotenv
import psycopg

load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_direct_connection():
    conn_str = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    print("Trying direct async connection to:", conn_str)

    try:
        async with await psycopg.AsyncConnection.connect(conninfo=conn_str) as conn:
            print("✅ Successfully connected to DB.")
    except Exception as e:
        print("❌ Direct connection failed.")
        print("🔍 Type:", type(e).__name__)
        print("🧨 Error:", str(e))


