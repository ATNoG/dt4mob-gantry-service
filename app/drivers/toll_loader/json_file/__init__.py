from app.drivers.toll_loader.json_file.toll_loader import JsonFileTollLoader
from app.settings import settings
from app.settings.toll_loader import TollLoaderBackend

if settings.toll_loader.backend != TollLoaderBackend.JSON_FILE:
    raise RuntimeError(
        "Json file toll loader instantiated, but backend is not json-file"
    )

json_file_toll_loader = JsonFileTollLoader(settings.toll_loader)  # ty:ignore[invalid-argument-type]
