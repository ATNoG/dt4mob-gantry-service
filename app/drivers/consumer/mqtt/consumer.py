import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from amqtt.client import QOS_0, ApplicationMessage, ClientConfig, MQTTClient
from amqtt.contexts import ConnectionConfig
from loguru import logger

from app.drivers.consumer import ConsumerMessage
from app.interface.consumer import ConsumerInterface
from app.settings.consumer import MQTTConsumerSettings


class MQTTConsumerInterface(ConsumerInterface):
    def __init__(
        self,
        *,
        advanced_settings: MQTTConsumerSettings,
        queue: asyncio.Queue[ConsumerMessage],
    ):
        super().__init__(advanced_settings=advanced_settings)
        self.settings = advanced_settings
        self.mqttc = MQTTClient(
            config=ClientConfig(
                connection=ConnectionConfig(uri=self.settings.get_uri()),
                reconnect_retries=-1,
            )
        )
        self.queue = queue

    @asynccontextmanager
    async def _resource(self) -> AsyncGenerator[None, None]:

        await self.mqttc.connect()
        await self.mqttc.subscribe(
            (topic, QOS_0) for topic in self.message_settings.keys()
        )

        yield

        await self.mqttc.disconnect()

    async def _messages(self) -> AsyncGenerator[ApplicationMessage, None]:
        while True:
            msg = await self.mqttc.deliver_message()
            if msg:
                yield msg

    async def loop(self) -> None:
        async with self._resource():
            async for msg in self._messages():
                logger.debug("Received message from: {topic}", topic=msg.topic)
                logger.debug("Content: {content}", content=msg.data)

                message_config = self.message_settings[msg.topic]

                await self.queue.put(
                    ConsumerMessage(
                        message_settings=message_config,
                        content=bytes(msg.data),
                    )
                )
                logger.trace("Queue: {}", self.queue)
