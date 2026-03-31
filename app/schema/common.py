from typing import Annotated, Optional, Self

from pydantic import BaseModel, ConfigDict, Field

Latitude = Annotated[float, Field(ge=-90.0, le=90.0)]

Longitude = Annotated[float, Field(ge=-180.0, le=180.0)]

type TupleCoordinates = tuple[Latitude, Longitude]

type NonEmptyStr = Annotated[str, Field(min_length=1)]


class LocalCoordinates(BaseModel):
    x: float
    y: float


class AbsoluteCoordinates(BaseModel):
    latitude: float
    longitude: float

    @classmethod
    def from_tuple(cls, coord_tuple: TupleCoordinates) -> Self:
        return cls(latitude=coord_tuple[0], longitude=coord_tuple[1])


class Dimensions(BaseModel):
    width: Optional[float] = None
    length: Optional[float] = None
    height: Optional[float] = None


class Empty(BaseModel):
    model_config = ConfigDict(extra="forbid")
