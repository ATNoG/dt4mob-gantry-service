from enum import Enum
from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, Field

from app.settings.message import MessageSettings


class ConsumerBackend(str, Enum):
    MQTT = "mqtt"
    Webhook = "webhook"


class BaseConsumerSettings(BaseModel):
    enabled: bool = True
    message_settings: List[MessageSettings] = []


class MQTTConsumerSettings(BaseConsumerSettings):
    backend: Literal[ConsumerBackend.MQTT] = ConsumerBackend.MQTT

    host: Annotated[str, Field(min_length=1)] = "127.0.0.1"
    port: Annotated[int, Field(ge=0, le=65535)] = 1883

    secure: bool = False

    username: Optional[str] = None
    password: Optional[str] = None

    def get_uri(self) -> str:
        url = ["mqtt"]

        if self.secure:
            url.append("s")

        url.append("://")

        if self.username and self.password:
            url.append(f"{self.username}:{self.password}@")

        url.append(f"{self.host}:{self.port}")
        return "".join(url)


class WebhookConsumerSettings(BaseConsumerSettings):
    backend: Literal[ConsumerBackend.Webhook] = ConsumerBackend.Webhook

    host: Annotated[str, Field(min_length=1)] = "127.0.0.1"
    port: Annotated[int, Field(ge=0, le=65535)] = 8000


type ConsumerSettings = Annotated[
    MQTTConsumerSettings | WebhookConsumerSettings, Field(discriminator="backend")
]
