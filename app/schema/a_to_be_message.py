from enum import StrEnum
from typing import Annotated, Optional

from pydantic import AwareDatetime, BaseModel, Field

from app.schema.common import (
    AbsoluteCoordinates,
    Dimensions,
    LocalCoordinates,
)

Timestamp = AwareDatetime


class ORTTrackingMessageBase(BaseModel):
    objectID: int
    triggeringTimestamp: Optional[Timestamp] = None


class CoordinateReference(StrEnum):
    right_rear_bottom_corner = "right_rear_bottom_corner"
    right_front_bottom_corner = "right_front_bottom_corner"


class PathItem(BaseModel):
    timeOfMeasurement: Timestamp
    speedKmh: Optional[float] = None
    coordinatesReference: Optional[CoordinateReference] = (
        CoordinateReference.right_rear_bottom_corner
    )
    localCoordinates: LocalCoordinates
    absoluteCoordinates: AbsoluteCoordinates
    dimensions: Dimensions


class ORTTrackingHistoryMessage(ORTTrackingMessageBase):
    path: Annotated[list[PathItem], Field(min_length=1)]


class ORTTrackingRealtimeMessage(ORTTrackingMessageBase, PathItem):
    pass
