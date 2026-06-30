from enum import Enum
from pathlib import Path
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field

from app.schema.common import NonEmptyStr


class SenderBackend(str, Enum):
    Disabled = "disabled"
    MQTT = "mqtt"
    HTTP = "http"


class BaseSenderSettings(BaseModel):
    pass


class DisabledSenderSettings(BaseSenderSettings):
    backend: Literal[SenderBackend.Disabled] = SenderBackend.Disabled


class MQTTSenderSettings(BaseSenderSettings):
    backend: Literal[SenderBackend.MQTT] = SenderBackend.MQTT

    host: Annotated[str, Field(min_length=1)] = "localhost"
    port: Annotated[int, Field(ge=0, le=65535)] = 1883

    username: Optional[str] = None
    password: Optional[str] = None

    cafile: Optional[Path] = None
    certfile: Optional[Path] = None
    keyfile: Optional[Path] = None

    tls: bool = True

    publish_topic: str = "telemetry"

    def get_uri(self) -> str:
        url = ["mqtt"]

        if self.tls:
            url.append("s")

        url.append("://")

        if self.username and self.password:
            url.append(f"{self.username}:{self.password}@")

        url.append(f"{self.host}:{self.port}")
        return "".join(url)


class HTTPSenderSettings(BaseSenderSettings):
    backend: Literal[SenderBackend.HTTP] = SenderBackend.HTTP

    host: NonEmptyStr = "localhost"
    port: Annotated[int, Field(ge=0, le=65535)] = 443

    username: Optional[str] = None
    password: Optional[str] = None

    tls: bool = False
    cafile: Optional[Path] = None
    client_key: Optional[Path] = None
    client_crt: Optional[Path] = None

    base_path: str = "/telemetry"

    def get_url(self) -> str:
        url = ["http"]

        if self.tls:
            url.append("s")

        url.append("://")

        if self.username and self.password:
            url.append(f"{self.username}:{self.password}@")

        url.append(f"{self.host}:{self.port}/{self.base_path.strip('/')}")
        return "".join(url)


type SenderSettings = Annotated[
    DisabledSenderSettings | MQTTSenderSettings | HTTPSenderSettings,
    Field(discriminator="backend"),
]
