import queue
import threading
from typing import Dict

from services.notifications.notification_strategy import NotificationStrategy

push_queue = queue.Queue()


class PushNotification(NotificationStrategy):
    _instance = None  # This will store the single instance of the class

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of EmailNotification is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.start_worker()  # Start the worker thread only once when the singleton is created
        return cls._instance

    async def init(self) -> None:
        pass


    async def send(self, recipient: str,  message: Dict) -> None:
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
        if not any(thread.name == 'PushWorker' for thread in threading.enumerate()):
            thread = threading.Thread(target=self.worker, daemon=True, name='PushWorker')
            thread.start()

    async def quit(self):
        pass