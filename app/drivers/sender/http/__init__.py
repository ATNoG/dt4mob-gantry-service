from app.settings import settings
from app.settings.sender import SenderBackend

from .sender import HTTPSenderInterface

if settings.sender.backend != SenderBackend.HTTP:
    raise RuntimeError("HTTP Sender driver instantiated but backend isn't HTTP")

http_sender_interface = HTTPSenderInterface(http_settings=settings.sender)
