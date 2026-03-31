from abc import ABC, abstractmethod

from app.interface.sender import SenderInterface


class TollLoaderInterface(ABC):

    @abstractmethod
    async def load(self, sender: SenderInterface) -> None:
        pass
