from typing import Optional

from app.interface.toll_loader import TollLoaderInterface
from app.settings import settings
from app.settings.toll_loader import TollLoaderBackend

toll_loader: Optional[TollLoaderInterface] = None

match settings.toll_loader.backend:
    case TollLoaderBackend.JSON_FILE:
        from .json_file import json_file_toll_loader

        toll_loader = json_file_toll_loader


def get_toll_loader() -> Optional[TollLoaderInterface]:
    return toll_loader
