from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, NonNegativeFloat

type Coord = Tuple[float, float]  # Not geographical coordinates
type BoundingSquare = Tuple[Coord, Coord, Coord, Coord]


class Alert(BaseModel):
    object_id: int
    class_name: str
    speed: NonNegativeFloat
    coordinate: BoundingSquare
    height: NonNegativeFloat
    zone_name: str
    speed_vector: Tuple[float, float, float]


class Data(BaseModel):
    in_alert: Alert
    out_alert: Optional[Alert]


class OutsightMessage(BaseModel):
    id: str
    type: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime]
    data: Data
