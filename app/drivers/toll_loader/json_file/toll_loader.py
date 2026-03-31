from loguru import logger

from app.interface.sender import SenderInterface
from app.interface.toll_loader import TollLoaderInterface
from app.schema.ditto import DittoProtocolEnvelope
from app.schema.toll import Tolls
from app.settings import settings
from app.settings.toll_loader import JsonFileTollLoaderSettings


class JsonFileTollLoader(TollLoaderInterface):
    def __init__(self, advanced_settings: JsonFileTollLoaderSettings) -> None:
        self.settings = advanced_settings

    async def load(self, sender: SenderInterface) -> None:
        with open(self.settings.filepath, "rb") as json_file:
            tolls = Tolls.model_validate_json(json_file.read()).tolls
        logger.debug(tolls)
        for toll in tolls:
            await sender.send(
                DittoProtocolEnvelope(
                    topic=f"{settings.ditto.namespace}/toll-{toll.id}/things/twin/commands/create",
                    path="/",
                    value={
                        "policyId": settings.ditto.policy_id,
                        "attributes": {
                            "id": toll.id,
                            "name": toll.name,
                            "coordinates": toll.coords,
                        },
                        "features": {
                            sensor: {"properties": {}} for sensor in toll.sensors
                        },
                    },
                )
                .model_dump_json(exclude_unset=True)
                .encode()
            )
        logger.info("Tolls loaded")
