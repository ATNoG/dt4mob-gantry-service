from enum import Enum
from typing import Annotated, Dict, Literal, Optional

from pydantic import BaseModel, Field, JsonValue

from app.settings.message import MessageSettings


class VehicleMessageType(str, Enum):
    DATA = "data"
    DELETE = "delete"


class BaseVehicleMessage(BaseModel):
    message_settings: MessageSettings
    id: int

    def prefix_id(self, id: Optional[int] = None) -> str:
        return f"{self.message_settings.source_name}.{id if id else self.id}"


class VehicleDataMessage(BaseVehicleMessage):
    message_type: Literal[VehicleMessageType.DATA] = VehicleMessageType.DATA
    data: Dict[str, JsonValue]


class VehicleDeleteMessage(BaseVehicleMessage):
    message_type: Literal[VehicleMessageType.DELETE] = VehicleMessageType.DELETE
    data: Optional[Dict[str, JsonValue]] = None


type VehicleMessage = Annotated[
    VehicleDataMessage | VehicleDeleteMessage, Field(discriminator="message_type")
]
