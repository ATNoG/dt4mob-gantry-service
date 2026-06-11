import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Set

from pydantic import BaseModel, JsonValue, RootModel

from app.interface.envelope_formatter import EnvelopeFormatterInterface
from app.schema.ditto import DittoMessage, DittoProtocolEnvelope, Headers
from app.schema.vehicle_message import (
    VehicleDataMessage,
    VehicleDeleteMessage,
    VehicleMessage,
    VehicleMessageType,
)
from app.settings import settings


class Attributes(BaseModel):
    id: int
    expiry_ts: datetime


class Properties(BaseModel):
    properties: dict[str, JsonValue] = dict()


Features = RootModel[dict[str, Properties]]


class FutureThing(BaseModel):
    attributes: Attributes
    features: Features
    policyId: str


class DittoThingEnvelopeFormatter(EnvelopeFormatterInterface):
    def __init__(
        self,
    ) -> None:
        self.config = settings.ditto_thing_settings

        self.delete_list: list[int] = []
        self.buffer_list: list[int] = []

        self.future_ids: Set[int] = set()

    def _add_future_id(self, id: int) -> Optional[list[int]]:
        delete_buffer_size = 50
        self.future_ids.add(id)
        if len(self.delete_list) < delete_buffer_size:
            self.delete_list.append(id)
        else:
            self.buffer_list.append(id)

        if len(self.buffer_list) >= delete_buffer_size:
            delete_list = self.delete_list
            self.delete_list = self.buffer_list
            self.buffer_list = []
            return delete_list
        return None

    def _handle_data(self, data_message: VehicleDataMessage) -> DittoMessage:
        correlation_id = str(uuid.uuid4())
        id = data_message.id

        update_envelope = DittoProtocolEnvelope(
            topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:{data_message.prefix_id()}/things/twin/commands/modify",
            headers=Headers(correlation_id=correlation_id),
            path="/features/State/properties/",
            value=data_message.data,
        )

        expire_at = datetime.now(tz=timezone.utc) + timedelta(seconds=30)
        update_expiry = DittoProtocolEnvelope(
            topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:{data_message.prefix_id()}/things/twin/commands/modify",
            headers=Headers(correlation_id=correlation_id),
            path="/attributes/expiry_ts",
            value=expire_at,
        )

        expire_at += timedelta(minutes=10)
        future_thing = FutureThing(
            policyId=settings.ditto.policy_id,
            attributes=Attributes(
                id=id + self.config.deferred_creation_offset, expiry_ts=expire_at
            ),
            features=Features({"State": Properties()}),
        )

        future_id = data_message.prefix_id(future_thing.attributes.id)
        future_envelope = DittoProtocolEnvelope(
            topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:{future_id}/things/twin/commands/create",
            headers=Headers(correlation_id=correlation_id),
            path="/",
            value=future_thing,
        )

        message = []

        if id in self.future_ids:
            message.append(update_envelope)
            message.append(update_expiry)

        if future_thing.attributes.id not in self.future_ids:
            message.append(future_envelope)
            delete_ids = self._add_future_id(future_thing.attributes.id)
            if delete_ids:
                message.extend(
                    (
                        DittoProtocolEnvelope(
                            topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:{data_message.prefix_id(id)}/things/twin/commands/delete",
                            headers=Headers(correlation_id=correlation_id),
                            path="/",
                        )
                        for id in delete_ids
                        if id in self.future_ids
                    )
                )
                self.future_ids.difference_update(delete_ids)

        return message

    def _handle_delete(self, delete_message: VehicleDeleteMessage) -> DittoMessage:
        correlation_id = str(uuid.uuid4())
        self.future_ids.discard(delete_message.id)
        return [
            DittoProtocolEnvelope(
                topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:{delete_message.prefix_id()}/things/twin/commands/delete",
                headers=Headers(correlation_id=correlation_id),
                path="/",
            )
        ]

    async def format(self, vehicle_message: VehicleMessage) -> DittoMessage:
        match vehicle_message.message_type:
            case VehicleMessageType.DATA:
                return self._handle_data(vehicle_message)  # ty:ignore[invalid-argument-type]
            case VehicleMessageType.DELETE:
                return self._handle_delete(vehicle_message)  # ty:ignore[invalid-argument-type]
