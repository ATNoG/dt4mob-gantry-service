from abc import ABC, abstractmethod

from app.settings.consumer import ConsumerSettings


class ConsumerInterface(ABC):

    def __init__(self, *, advanced_settings: ConsumerSettings) -> None:
        self.message_settings = {
            message_config.topic: message_config
            for message_config in advanced_settings.message_settings
        }

    @abstractmethod
    async def loop(self) -> None:
        pass
