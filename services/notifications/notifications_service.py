import threading
from abc import ABC, abstractmethod
from typing import Dict, Optional
import queue

email_queue = queue.Queue()
push_queue = queue.Queue()

class NotificationStrategy(ABC):

    @abstractmethod
    def send(self, recipient: str, message: Dict) -> None:
        ...

    @abstractmethod
    def worker(self):
        ...

    @abstractmethod
    def start_worker(self):
        ...

class EmailNotification(NotificationStrategy):

    def send(self, recipient: str,  message: Dict) -> None:
        email_queue.put(message)


    def worker(self):
        """
        This worker thread will continuously check the queue for email tasks and process them.
        """
        while True:
            email = email_queue.get()  # Block until an email task is available
            print(f"This message sent from email {email}")
            if email is None:
                break  # None is used to signal the thread to stop
            email_queue.task_done()

    def start_worker(self):
        thread = threading.Thread(target=self.worker, daemon=True)
        thread.start()


class PushNotification(NotificationStrategy):

    def send(self, recipient: str,  message: Dict) -> None:
        push_queue.put(message)

    def worker(self):
        """
        This worker thread will continuously check the queue for push tasks and process them.
        """
        while True:
            push = push_queue.get()  # Block until an email task is available
            print(f"This message sent from push {push}")
            if push is None:
                break  # None is used to signal the thread to stop
            push_queue.task_done()

    def start_worker(self):
        thread = threading.Thread(target=self.worker, daemon=True)
        thread.start()


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