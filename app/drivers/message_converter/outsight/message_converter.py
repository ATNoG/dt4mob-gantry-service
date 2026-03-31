from typing import Optional, Set

from loguru import logger
from pydantic import ValidationError

from app.interface.message_converter import MessageConverterInterface
from app.schema.outsight_message import OutsightMessage
from app.schema.vehicle_message import VehicleDataMessage, VehicleMessage
from app.settings.message import OutSightMessageSettings


class OutsightMessageConverter(MessageConverterInterface):
    def __init__(self) -> None:
        # This will be used for the case when messages come out of order
        self.message_seen: Set[str] = set()

    def _handle_message(
        self, content: bytes, message_settings: OutSightMessageSettings
    ) -> Optional[VehicleMessage]:
        outsight_message = OutsightMessage.model_validate_json(content)

        is_not_final = outsight_message.data.out_alert is None
        if outsight_message.id in self.message_seen:
            self.message_seen.remove(outsight_message.id)
            if is_not_final:
                return None
        else:
            self.message_seen.add(outsight_message.id)

        return VehicleDataMessage(
            id=outsight_message.data.in_alert.object_id,
            data=outsight_message.model_dump(mode="json"),
            message_settings=message_settings,
        )

    def convert(
        self, content: bytes, message_settings: OutSightMessageSettings
    ) -> Optional[VehicleMessage]:
        try:
            return self._handle_message(content, message_settings)
        except ValidationError:
            logger.warning(
                "Incorrect message received on topic '{}' and source '{}' for the OutSight converter",
                message_settings.topic,
                message_settings.source_name,
            )
            return None
