import asyncio
from asyncio import Task
from typing import Optional

from amqtt.client import ClientConfig, MQTTClient
from amqtt.contexts import ConnectionConfig
from loguru import logger

from app.interface.sender import SenderInterface
from app.settings.sender import MQTTSenderSettings


class MQTTSenderInterface(SenderInterface):
    def __init__(self, mqtt_settings: MQTTSenderSettings) -> None:
        self.mqttc = MQTTClient(
            config=ClientConfig(
                reconnect_retries=-1,
                connection=ConnectionConfig(
                    cafile=mqtt_settings.cafile,
                    certfile=mqtt_settings.certfile,
                    keyfile=mqtt_settings.keyfile,
                    uri=mqtt_settings.get_uri(),
                ),
            )
        )
        self._reconnect_task: Optional[Task] = None

    async def _reconnect_loop(self):
        while True:
            await asyncio.sleep(150)
            logger.debug("Attempt manual reconnection")
            await self.mqttc.disconnect()
            await self.mqttc.connect()

    async def start(self) -> None:
        await self.mqttc.connect()
        self._reconnect_task = asyncio.create_task(self._reconnect_loop())

    async def stop(self) -> None:
        if self._reconnect_task:
            self._reconnect_task.cancel()
            self._reconnect_task = None
        await self.mqttc.disconnect()

    async def send(self, payload: bytes) -> None:
        logger.debug("Sending: {payload}", payload=payload)
        await self.mqttc.publish("telemetry", payload)
