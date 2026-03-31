from app.settings import settings
from app.settings.sender import SenderBackend

from .sender import MQTTSenderInterface

if settings.sender.backend != SenderBackend.MQTT:
    raise RuntimeError("MQTT Sender driver instantiated but backend isn't MQTT")

mqtt_sender_interface = MQTTSenderInterface(mqtt_settings=settings.sender)
