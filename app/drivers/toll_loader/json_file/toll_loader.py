from loguru import logger

from app.interface.sender import SenderInterface
from app.interface.toll_loader import TollLoaderInterface
from app.schema.ditto import DittoProtocolEnvelope
from app.schema.toll import Tolls
from app.settings import settings
from app.settings.toll_loader import JsonFileTollLoaderSettings
from app.utils.geo import get_geotile


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
                    topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:toll-{toll.id}/things/twin/commands/create",
                    path="/",
                    value={
                        "policyId": settings.ditto.policy_id,
                        "attributes": {
                            "id": toll.id,
                            "name": toll.name,
                            "coordinates": toll.coords,
                            "geotile": get_geotile(
                                toll.coords.latitude, toll.coords.longitude
                            ),
                            "dashboardUrl": toll.dashboardUrl,
                        },
                        "features": {
                            sensor: {"properties": {}} for sensor in toll.sensors
                        },
                    },
                )
                .model_dump_json(exclude_unset=True, exclude_none=True)
                .encode()
            )
            for sensor in toll.sensors:
                await sender.send(
                    DittoProtocolEnvelope(
                        topic=f"{settings.ditto.namespace}/{settings.ditto.subject}:toll-{toll.id}/things/twin/commands/modify",
                        path=f"/features/{sensor}/properties",
                        value={},
                    )
                    .model_dump_json(exclude_unset=True)
                    .encode()
                )
        logger.info("Tolls loaded")
