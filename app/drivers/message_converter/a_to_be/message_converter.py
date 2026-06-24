from typing import Optional

from loguru import logger
from pydantic import ValidationError

from app.interface.message_converter import MessageConverterInterface
from app.schema.a_to_be_message import (
    ORTTrackingHistoryMessage,
    ORTTrackingRealtimeMessage,
)
from app.schema.vehicle_message import (
    VehicleDataMessage,
    VehicleDeleteMessage,
    VehicleMessage,
)
from app.settings.message import AToBeMessageSettings, AToBeMessageType


class AToBeMessageConverter(MessageConverterInterface):
    def __init__(self) -> None:
        logger.info("A-to-Be message converter instantiated")

    def _handle_realtime(
        self, content: bytes, message_settings: AToBeMessageSettings
    ) -> VehicleMessage:
        vehicle_message = ORTTrackingRealtimeMessage.model_validate_json(content)

        return VehicleDataMessage(
            id=vehicle_message.objectID,
            data=vehicle_message.model_dump(mode="json", exclude_unset=True),
            message_settings=message_settings,
        )

    def _handle_history(
        self, content: bytes, message_settings: AToBeMessageSettings
    ) -> VehicleMessage:
        history_message = ORTTrackingHistoryMessage.model_validate_json(content)
        return VehicleDeleteMessage(
            id=history_message.objectID,
            timestamp_override=history_message.triggeringTimestamp,
            data=history_message.model_dump(mode="json", exclude_unset=True),
            message_settings=message_settings,
        )

    def convert(
        self, content: bytes, message_settings: AToBeMessageSettings
    ) -> Optional[VehicleMessage]:
        try:
            match message_settings.atobe_type:
                case AToBeMessageType.REALTIME:
                    return self._handle_realtime(content, message_settings)
                case AToBeMessageType.HISTORY:
                    return self._handle_history(content, message_settings)
        except ValidationError as e:
            logger.debug("{}", e)
            logger.warning(
                "Incorrect message received on topic '{}' and source '{}' for the A-to-Be converter",
                message_settings.topic,
                message_settings.source_name,
            )
            return None
