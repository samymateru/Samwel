import asyncio
from services.logging.logger import global_logger
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('SERVER_HOST')
PORT = os.getenv('SERVER_PORT')


async def tcp_client(host=HOST, port=PORT):
    reader, writer = await asyncio.open_connection(host, port)
    global_logger.info(f"CONNECTED TO SERVER AT {host}:{port}")

    try:
        async def read_from_server():
            while True:
                data = await reader.readline()
                if not data:
                    print("Server closed the connection")
                    break
                print(f"Server says: {data.decode().strip()}")


        async def send_to_server():
            while True:
                message = await asyncio.to_thread(input, "Enter message: ")
                if message.lower() == "exit":
                    writer.close()
                    await writer.wait_closed()
                    break
                writer.write((message + "\n").encode())


        await asyncio.gather(read_from_server(), send_to_server())

    except KeyboardInterrupt:
        global_logger.info("SOCKET CONNECTION CLOSED")

    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(tcp_client())
