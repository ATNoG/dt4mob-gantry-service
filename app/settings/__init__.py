import sys
from typing import List, Literal

from loguru import logger
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from app.settings.consumer import ConsumerSettings
from app.settings.ditto import DittoSettings
from app.settings.envelope_formatter import (
    DittoThingSettings,
    EnvelopeFormatterSettings,
)
from app.settings.message_converter import MessageConverterSettings
from app.settings.sender import DisabledSenderSettings, SenderSettings
from app.settings.toll_loader import DisabledTollLoaderSettings, TollLoaderSettings

LogLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="config.toml",
        env_prefix="GS_",
        env_nested_delimiter="__",
    )

    consumers: List[ConsumerSettings] = []

    message_converters: MessageConverterSettings = MessageConverterSettings()
    envelope_formatters: EnvelopeFormatterSettings = EnvelopeFormatterSettings()
    ditto_thing_settings: DittoThingSettings = DittoThingSettings()

    sender: SenderSettings = DisabledSenderSettings()

    toll_loader: TollLoaderSettings = DisabledTollLoaderSettings()

    ditto: DittoSettings = DittoSettings()
    log_level: LogLevel = "INFO"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            TomlConfigSettingsSource(settings_cls),
        )


settings = Settings()

logger.remove()
logger.add(sys.stdout, level=settings.log_level)

logger.debug(settings)
