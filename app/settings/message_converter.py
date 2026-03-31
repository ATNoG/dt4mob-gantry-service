from enum import Enum

from pydantic import RootModel


class MessageConverterBackend(str, Enum):
    AToBe = "a-to-be"
    OutSight = "outsight"


class MessageConverterSettings(RootModel[dict[MessageConverterBackend, bool]]):
    root: dict[MessageConverterBackend, bool] = dict()
