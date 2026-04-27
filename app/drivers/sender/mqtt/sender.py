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
                check_hostname=None,
                connection=ConnectionConfig(
                    cafile=mqtt_settings.cafile,
                    uri=mqtt_settings.get_uri(),
                ),
            )
        )

    async def start(self) -> None:
        await self.mqttc.connect()

    async def stop(self) -> None:
        await self.mqttc.disconnect()

    async def send(self, payload: bytes) -> None:
        logger.debug("Sending: {payload}", payload=payload)
        await self.mqttc.publish("telemetry", payload)
