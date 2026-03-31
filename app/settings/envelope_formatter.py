from enum import Enum

from pydantic import BaseModel, PositiveInt, RootModel


class EnvelopeFormatterBackend(str, Enum):
    TOLL_FEATURE = "toll-feature"
    DITTO_THING = "ditto-thing"


class EnvelopeFormatterSettings(RootModel[dict[EnvelopeFormatterBackend, bool]]):
    root: dict[EnvelopeFormatterBackend, bool] = dict()


class DittoThingSettings(BaseModel):
    deferred_creation_offset: PositiveInt = 10
