from abc import ABC, abstractmethod
from typing import Dict, Optional


class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, recipient: str, message: Dict) -> None:
        print(message)


class EmailNotification(NotificationStrategy):

    def send(self, recipient: str,  message: Dict) -> None:
        print("Email sent")
        pass

class PushNotification(NotificationStrategy):

    def send(self, recipient: str,  message: Dict) -> None:
        print("Push sent")
        pass


class NotificationManager:
    def __init__(self):
        self._strategy: Optional[NotificationStrategy] = None

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def get_strategy(self) -> Optional[NotificationStrategy]:
        return self._strategy

    def notify(self, recipient, message):
        if self.get_strategy() is not None:
            self._strategy.send(recipient, message)
        else:
            raise RuntimeError("Provide notification strategy")