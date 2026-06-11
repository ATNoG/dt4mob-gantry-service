import uuid
from typing import Optional

from app.interface.envelope_formatter import EnvelopeFormatterInterface
from app.schema.ditto import DittoMessage, DittoProtocolEnvelope, Headers
from app.schema.vehicle_message import (
    VehicleDataMessage,
    VehicleDeleteMessage,
    VehicleMessage,
    VehicleMessageType,
)
from app.settings import settings


class TollFeatureEnvelopeFormatter(EnvelopeFormatterInterface):
    def __init__(self) -> None:
        self._delete_ids: list[int] = []
        self._buffer_ids: list[int] = []
        self._existing_ids: set[int] = set()

    def _add_id(self, id: int) -> Optional[list[int]]:
        self._existing_ids.add(id)
        delete_buffer_size = 50
        if len(self._delete_ids) < delete_buffer_size:
            self._delete_ids.append(id)
        else:
            self._buffer_ids.append(id)

        if len(self._buffer_ids) >= delete_buffer_size:
            delete_ids = self._delete_ids
            self._delete_ids = self._buffer_ids
            self._buffer_ids = []
            return delete_ids

        return None

    def _handle_data(self, data_message: VehicleDataMessage) -> DittoMessage:
        correlation_id = str(uuid.uuid4())

        message = [
            DittoProtocolEnvelope(
                topic=f"{settings.ditto.namespace}/toll-{settings.ditto.toll_id}/things/twin/commands/modify",
                headers=Headers(correlation_id=correlation_id),
                path=f"/features/{data_message.message_settings.source_name}/properties/{data_message.id}",
                value=data_message.data,
            )
        ]

        if data_message.id not in self._existing_ids:
            delete_ids = self._add_id(data_message.id)
            if delete_ids:
                message.extend(
                    (
                        DittoProtocolEnvelope(
                            topic=f"{settings.ditto.namespace}/toll-{settings.ditto.toll_id}/things/twin/commands/delete",
                            headers=Headers(correlation_id=correlation_id),
                            path=f"/features/{data_message.message_settings.source_name}/properties/{id}",
                        )
                        for id in delete_ids
                        if id in self._existing_ids
                    )
                )
                self._existing_ids.difference_update(delete_ids)

        return message

    def _handle_delete(self, delete_message: VehicleDeleteMessage) -> DittoMessage:
        correlation_id = str(uuid.uuid4())
        self._existing_ids.discard(delete_message.id)

        message = [
            DittoProtocolEnvelope(
                topic=f"{settings.ditto.namespace}/toll-{settings.ditto.toll_id}/things/twin/commands/delete",
                headers=Headers(correlation_id=correlation_id),
                path=f"/features/{delete_message.message_settings.source_name}/properties/{delete_message.id}",
            )
        ]

        if delete_message.data is not None:
            message.append(
                DittoProtocolEnvelope(
                    topic=f"{settings.ditto.namespace}/toll-{settings.ditto.toll_id}/things/twin/commands/modify",
                    headers=Headers(correlation_id=correlation_id),
                    path=f"/features/{delete_message.message_settings.source_name}/properties/historic",
                    value=delete_message.data,
                )
            )

        return message

    async def format(self, vehicle_message: VehicleMessage) -> DittoMessage:
        match vehicle_message.message_type:
            case VehicleMessageType.DATA:
                return self._handle_data(vehicle_message)  # ty:ignore[invalid-argument-type]
            case VehicleMessageType.DELETE:
                return self._handle_delete(vehicle_message)  # ty:ignore[invalid-argument-type]
