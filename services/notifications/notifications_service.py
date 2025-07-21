from abc import ABC, abstractmethod
from typing import Dict


class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, recipient: str, message: Dict) -> None:
        print(message)


class EmailNotification(NotificationStrategy):

    def send(self, recipient: str,  message: Dict) -> None:
        pass

class PushNotification(NotificationStrategy):

    def send(self, recipient: str,  message: Dict) -> None:
        pass


class NotificationManager:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notify(self, recipient, message):
        self.strategy.send(recipient, message)