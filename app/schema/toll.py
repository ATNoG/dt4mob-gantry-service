from typing import Annotated, Optional

from pydantic import AnyHttpUrl, BaseModel, Field

from app.schema.common import AbsoluteCoordinates


class Toll(BaseModel):
    id: int
    name: str
    coords: AbsoluteCoordinates
    sensors: set[str]
    dashboardUrl: Annotated[
        Optional[AnyHttpUrl],
        Field(description="Grafana dashboard URL with toll related information"),
    ] = None


class Tolls(BaseModel):
    tolls: list[Toll]
