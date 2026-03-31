from abc import ABC, abstractmethod

from app.schema.ditto import DittoMessage
from app.schema.vehicle_message import VehicleMessage


class EnvelopeFormatterInterface(ABC):

    @abstractmethod
    async def format(self, vehicle_message: VehicleMessage) -> DittoMessage:
        pass
