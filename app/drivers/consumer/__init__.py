import asyncio
from typing import List

from loguru import logger
from pydantic import BaseModel

from app.interface.consumer import ConsumerInterface
from app.settings import settings
from app.settings.consumer import ConsumerBackend
from app.settings.message import MessageSettings


class ConsumerMessage(BaseModel):
    message_settings: MessageSettings
    content: bytes


queue: asyncio.Queue[ConsumerMessage] = asyncio.Queue()
consumers: List[ConsumerInterface] = []

for consumer_settings in settings.consumers:
    if not consumer_settings.enabled:
        continue

    if any(
        len(message_config.allowed_ditto_formats) == 0
        for message_config in consumer_settings.message_settings
    ):
        logger.warning(
            "There is a consumer with backend '{}' that has messages with no allowed Ditto formats. This means those messages will never reach Ditto",
            consumer_settings.backend.value,
        )

    match consumer_settings.backend:
        case ConsumerBackend.MQTT:
            from .mqtt.consumer import MQTTConsumerInterface

            consumers.append(
                MQTTConsumerInterface(advanced_settings=consumer_settings, queue=queue)
            )

        case ConsumerBackend.Webhook:
            from .webhook.consumer import WebhookConsumerInterface

            consumers.append(
                WebhookConsumerInterface(
                    advanced_settings=consumer_settings, queue=queue
                )
            )


def get_queue() -> asyncio.Queue[ConsumerMessage]:
    return queue


def get_consumers() -> List[ConsumerInterface]:
    return consumers
