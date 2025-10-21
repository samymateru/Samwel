from email.message import EmailMessage
from typing import Dict
from aiosmtplib import SMTP, SMTPException
import asyncio

from fastapi import HTTPException

from services.logging.logger import global_logger
from services.notifications.notification_strategy import NotificationStrategy

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "samymateru1999@gmail.com"
SENDER_PASSWORD = "eqdi kxuv vwmq fnth"

email_queue = asyncio.Queue()


class EmailNotification(NotificationStrategy):
    _instance = None
    _smtp = None
    _initialized = False
    _workers = False


    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of EmailNotification is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        # Ensure initialization is done only once
        if not hasattr(self, "_initialized"):
            super().__init__()


    async def init(self):
        """Initialize SMTP connection (only once)."""
        if self._initialized:
            return
        try:
            self._smtp = SMTP(hostname=SMTP_SERVER, port=SMTP_PORT, use_tls=True)
            await self._smtp.connect()
            await self._smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            self._initialized = True
            global_logger.info(f"✅ Successfully connected to the SMTP server.")
        except SMTPException as s:
            global_logger.critical(f"❌ Failed to connect to SMTP server: {s}")
            raise
        except Exception as e:
            global_logger.critical(f"❌ Error during establishing SMTP connection: {e}")
            raise


    async def send(self, recipient: str, message: Dict) -> None:
        """Put email tasks in the queue."""
        if not self._smtp.is_connected:
            raise HTTPException(status_code=400, detail="SMTP server not connected")
        await email_queue.put(message)


    async def worker(self):
        """
        This async worker will continuously check the queue for email tasks and process them.
        """
        while True:
            email = await email_queue.get()  # Use asyncio.to_thread for blocking calls
            if email is None:
                break  # None is used to signal the thread to stop
            try:
                msg = EmailMessage()
                msg['From'] = SENDER_EMAIL
                msg['To'] = email.get("To", "")
                msg['Subject'] = email.get("Subject", "")
                msg.set_content(email.get("Content", ""))
                await self._smtp.send_message(msg)
                global_logger.info(f"✅ Email successfully sent to {msg['To']}")
                email_queue.task_done()
                await asyncio.sleep(1)
            except SMTPException as e:
                self._initialized = False
                await self.init()
                await self.send(recipient="", message=email)
                global_logger.critical(f"❌ Failed to send email to smtp {email['To']} with error {e}")
            except Exception as e:
                global_logger.critical(f"❌ Failed to send email to {email['To']} with error {e}")
                raise HTTPException(status_code=400, detail="Error connecting smtp server")


    async def start_worker(self):
        if self._workers:
            return
        if not any(task.get_name() == 'EmailWorker' for task in asyncio.all_tasks()):
            asyncio.create_task(self.worker(), name='EmailWorker')
            self._workers = True


    async def quit(self):
        """Gracefully close the SMTP connection."""
        if self._smtp:
            await self._smtp.quit()
            global_logger.info(f"✅ SMTP connection closed.")