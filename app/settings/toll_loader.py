from enum import StrEnum
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class TollLoaderBackend(StrEnum):
    DISABLED = "disabled"
    JSON_FILE = "json-file"


class BaseTollLoaderSettings(BaseModel):
    pass


class DisabledTollLoaderSettings(BaseTollLoaderSettings):
    backend: Literal[TollLoaderBackend.DISABLED] = TollLoaderBackend.DISABLED


class JsonFileTollLoaderSettings(BaseTollLoaderSettings):
    backend: Literal[TollLoaderBackend.JSON_FILE] = TollLoaderBackend.JSON_FILE

    filepath: Path = Path("tolls.json")


type TollLoaderSettings = Annotated[
    DisabledTollLoaderSettings | JsonFileTollLoaderSettings,
    Field(discriminator="backend"),
]
