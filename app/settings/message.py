from enum import StrEnum
from typing import Annotated, Literal, Set

from pydantic import BaseModel, Field

from app.schema.common import NonEmptyStr
from app.settings.envelope_formatter import EnvelopeFormatterBackend
from app.settings.message_converter import MessageConverterBackend


class BaseMessageSettings(BaseModel):
    enabled: bool = True
    topic: NonEmptyStr
    source_name: NonEmptyStr
    allowed_ditto_formats: Set[EnvelopeFormatterBackend] = set()


class OutSightMessageSettings(BaseMessageSettings):
    expected_message_type: Literal[MessageConverterBackend.OutSight] = (
        MessageConverterBackend.OutSight
    )


class AToBeMessageType(StrEnum):
    REALTIME = "realtime"
    HISTORY = "history"


class AToBeMessageSettings(BaseMessageSettings):
    expected_message_type: Literal[MessageConverterBackend.AToBe] = (
        MessageConverterBackend.AToBe
    )
    atobe_type: AToBeMessageType


type MessageSettings = Annotated[
    AToBeMessageSettings | OutSightMessageSettings,
    Field(discriminator="expected_message_type"),
]
