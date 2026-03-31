from typing import Optional

from app.interface.sender import SenderInterface
from app.settings import settings
from app.settings.sender import SenderBackend

sender_interface: Optional[SenderInterface] = None
match settings.sender.backend:
    case SenderBackend.MQTT:
        from .mqtt import mqtt_sender_interface

        sender_interface = mqtt_sender_interface

    case SenderBackend.HTTP:
        from .http import http_sender_interface

        sender_interface = http_sender_interface


def get_sender_interface() -> Optional[SenderInterface]:
    return sender_interface
