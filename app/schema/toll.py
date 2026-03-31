from pydantic import BaseModel

from app.schema.common import AbsoluteCoordinates


class Toll(BaseModel):
    id: int
    name: str
    coords: AbsoluteCoordinates
    sensors: set[str]


class Tolls(BaseModel):
    tolls: list[Toll]
