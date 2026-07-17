import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import AsyncGenerator

from amqtt.client import QOS_0, ApplicationMessage, ClientConfig, MQTTClient
from amqtt.contexts import ConnectionConfig
from amqtt.errors import ClientError
from amqtt.utils import gen_client_id
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

        self.last_message_time: datetime = datetime.now()

    @asynccontextmanager
    async def _resource(self) -> AsyncGenerator[None, None]:

        await self.mqttc.connect()
        await self.mqttc.subscribe(
            (topic, QOS_0) for topic in self.message_settings.keys()
        )

        reconnect_task = asyncio.create_task(self._reconnect_watch_dog())

        yield

        reconnect_task.cancel()

        await self.mqttc.disconnect()

    async def _messages(self) -> AsyncGenerator[ApplicationMessage, None]:
        while True:
            try:
                msg = await self.mqttc.deliver_message()
                if msg is not None:
                    yield msg
            except ClientError:
                logger.warning("Consumer disconnected, attempting to reconnect")
                await self.mqttc.connect()

    async def _reconnect_watch_dog(self):
        while True:
            logger.debug("Watching")
            if (datetime.now() - self.last_message_time) > timedelta(minutes=5):
                logger.info("Reconnect consumer")
                await self.mqttc.disconnect()
                self.mqttc.client_id = gen_client_id()
                logger.debug(
                    "Connect code: {}", await self.mqttc.connect(cleansession=True)
                )
            await asyncio.sleep(150)

    async def loop(self) -> None:
        async with self._resource():
            async for msg in self._messages():
                logger.debug("Received message from: {topic}", topic=msg.topic)
                logger.debug("Content: {content}", content=msg.data)

                message_config = self.message_settings[msg.topic]

                self.last_message_time = datetime.now()
                await self.queue.put(
                    ConsumerMessage(
                        message_settings=message_config,
                        content=bytes(msg.data),
                    )
                )
                logger.trace("Queue: {}", self.queue)
