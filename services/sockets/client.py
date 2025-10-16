import asyncio
from services.logging.logger import global_logger
from dotenv import load_dotenv
import os

load_dotenv()


class SocketClient:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SocketClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.host = os.getenv('SERVER_HOST')
        self.port = int(os.getenv('SERVER_PORT'))
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self.read_task: asyncio.Task | None = None
        self._lock = asyncio.Lock()
        self._connected = False

    async def connect(self):
        """Connect to the TCP server and start the reader loop."""
        async with self._lock:
            if self._connected:
                global_logger.info("Already connected to server")
                return

            try:
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                self._connected = True
                global_logger.info(f"Connected to server at {self.host}:{self.port}")

                # Start background reading loop
                self.read_task = asyncio.create_task(self._read_from_server())
            except Exception as e:
                global_logger.exception(f"Failed to connect: {e}")
                raise

    async def _read_from_server(self):
        """Continuously read messages from the server."""
        try:
            while True:
                data = await self.reader.readline()
                if not data:
                    global_logger.warning("Server closed the connection")
                    break
                message = data.decode().strip()
                global_logger.info(f"Server says: {message}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            global_logger.error(f"Error reading from server: {e}")
        finally:
            self._connected = False


    async def send_message(self, message: str):
        """Send a message to the server."""
        if not self._connected or not self.writer:
            global_logger.exception("Not connected to server")

        self.writer.write((message + "\n").encode())
        await self.writer.drain()


    async def close(self):
        """Gracefully close the connection."""
        async with self._lock:
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()
                global_logger.info("Connection closed")

            if self.read_task:
                self.read_task.cancel()

            self._connected = False
            self.writer = None
            self.reader = None


# ✅ Expose a global instance for import
socket_client = SocketClient()
