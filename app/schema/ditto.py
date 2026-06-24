from datetime import datetime
from typing import Annotated, Any, Dict, Iterable, List, Optional

from pydantic import BaseModel, ConfigDict, Field

RequestedAck = Annotated[str, Field(pattern=r"[a-zA-Z0-9-_:]{3,100}")]


class Headers(BaseModel):
    model_config = ConfigDict(validate_by_name=True, serialize_by_alias=True)

    content_type: Annotated[Optional[str], Field(alias="content-type")] = None
    correlation_id: Annotated[Optional[str], Field(alias="correlation-id")] = None
    ditto_originator: Annotated[Optional[str], Field(alias="ditto-originator")] = None
    If_Match: Annotated[Optional[str], Field(alias="If-Match")] = None
    If_None_Match: Annotated[Optional[str], Field(alias="If-None-Match")] = None
    if_equal: Annotated[Optional[str], Field(alias="if-equal")] = None
    response_required: Annotated[Optional[bool], Field(alias="response-required")] = (
        None
    )
    requested_acks: Annotated[
        Optional[List[RequestedAck]], Field(alias="requested-acks")
    ] = None
    timeout: Annotated[Optional[str], Field()] = None
    version: Annotated[Optional[int], Field(ge=1, le=2)] = None
    condition: Annotated[Optional[str], Field()] = None
    dt4mob_historic_timestamp_override: Annotated[
        Optional[datetime], Field(alias="dt4mob-historic-timestamp-override")
    ] = None


class DittoProtocolEnvelope(BaseModel):
    topic: str
    headers: Headers = Headers()
    path: str
    fields: Optional[str] = None
    value: Optional[Any] = None
    extra: Optional[Dict[str, Any]] = None

    # Events
    revision: Optional[float] = None
    timestamp: Optional[datetime] = None


type DittoMessage = Iterable[DittoProtocolEnvelope]
