from typing import Dict, Optional

from services.logging.logger import global_logger
from services.notifications.email_notification import EmailNotification
from services.notifications.notification_strategy import NotificationStrategy

class NotificationManager:
    _instance = None
    _strategy: Optional[NotificationStrategy] = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of NotificationManager is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._strategy = EmailNotification()
        return cls._instance


    async def start_worker(self):
        if self._strategy is None:
            global_logger.critical("The notification strategy is not found")
            raise RuntimeError("The notification strategy is not found")

        """Start the email worker"""
        await self._strategy.start_worker()

    async def connect(self):
        """Start the email worker"""
        try:

            await self._strategy.init()
        except Exception:
            raise


    async def set_strategy(self, strategy: NotificationStrategy):
        """Set the notification strategy (Email, Push, etc.)"""
        await self._strategy.init()
        await self._strategy.start_worker()
        self._strategy = strategy

    def get_strategy(self) -> Optional[NotificationStrategy]:
        """Get the current notification strategy"""
        return self._strategy

    async def notify(self, recipient: str, message: Dict):
        """Notify using the current strategy"""
        if self.get_strategy() is not None:
            try:
                await self._strategy.send(recipient, message)
            except Exception:
                raise
        else:
            raise RuntimeError("Provide notification strategy")

    async def quit(self):
        """Close the SMTP connection gracefully."""
        await self._strategy.quit()