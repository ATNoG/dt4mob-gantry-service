from typing import Optional

from app.settings import settings
from app.settings.message_converter import MessageConverterBackend

from .a_to_be.message_converter import AToBeMessageConverter
from .outsight.message_converter import OutsightMessageConverter


class MessageConverterStore:
    atobe_converter: Optional[AToBeMessageConverter] = None
    outsight_converter: Optional[OutsightMessageConverter] = None


message_converter_store = MessageConverterStore()

if settings.message_converters.root.get(MessageConverterBackend.AToBe):
    message_converter_store.atobe_converter = AToBeMessageConverter()

if settings.message_converters.root.get(MessageConverterBackend.OutSight):
    message_converter_store.outsight_converter = OutsightMessageConverter()


def get_message_converters() -> MessageConverterStore:
    return message_converter_store
