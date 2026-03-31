from abc import ABC, abstractmethod


class SenderInterface(ABC):

    @abstractmethod
    async def send(self, payload: bytes) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
