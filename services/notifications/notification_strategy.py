from abc import ABC, abstractmethod
from typing import Dict


class NotificationStrategy(ABC):

    @abstractmethod
    async def init(self) -> None:
        ...

    @abstractmethod
    async def send(self, recipient: str, message: Dict) -> None:
        ...

    @abstractmethod
    async def worker(self):
        ...

    @abstractmethod
    async def start_worker(self):
        ...

    @abstractmethod
    async def quit(self):
        ...