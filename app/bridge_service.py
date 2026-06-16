import asyncio
from asyncio.tasks import Task
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, List, Optional, Tuple

from loguru import logger

from app.drivers.consumer import ConsumerMessage, get_consumers, get_queue
from app.drivers.envelope_formatter import get_envelope_formatters
from app.drivers.message_converter import get_message_converters
from app.drivers.sender import get_sender_interface
from app.drivers.toll_loader import get_toll_loader
from app.interface.message_converter import MessageConverterInterface
from app.schema.ditto import DittoMessage
from app.schema.vehicle_message import VehicleMessage
from app.settings import settings
from app.settings.message_converter import MessageConverterBackend


class BridgeService:
    def __init__(self) -> None:
        self._message_queue = get_queue()
        self._send_queue: asyncio.Queue[DittoMessage] = asyncio.Queue()
        self._consumers = get_consumers()
        self._message_converter_store = get_message_converters()
        self._envelope_formatters = get_envelope_formatters()
        self._sender = get_sender_interface()
        self._toll_loader = get_toll_loader()

        self._message_converter_map: Dict[
            Tuple[str, str], MessageConverterInterface
        ] = dict()

    @asynccontextmanager
    async def _resources(self) -> AsyncGenerator[None, None]:
        tasks: List[asyncio.Task[None]] = []
        for consumer in self._consumers:
            tasks.append(asyncio.create_task(consumer.loop()))

        sender_loop_task: Optional[Task] = None
        if self._sender:
            await self._sender.start()
            sender_loop_task = asyncio.create_task(self._sender_loop())

        clear_task = asyncio.create_task(self._clear_loop())

        yield

        clear_task.cancel()

        if sender_loop_task is not None:
            sender_loop_task.cancel()

        if self._sender:
            await self._sender.stop()

        for task in tasks:
            task.cancel()

    async def _messages(self) -> AsyncGenerator[ConsumerMessage, None]:
        while True:
            yield await self._message_queue.get()

    def _convert_message(self, message: ConsumerMessage) -> Optional[VehicleMessage]:
        message_settings = message.message_settings
        content = message.content
        converter: Optional[MessageConverterInterface]
        match message_settings.expected_message_type:
            case MessageConverterBackend.AToBe:
                converter = self._message_converter_store.atobe_converter
                if not converter:
                    return None
                return converter.convert(content, message_settings)  # ty:ignore[invalid-argument-type]

            case MessageConverterBackend.OutSight:
                converter = self._message_converter_store.outsight_converter
                if not converter:
                    return None
                return converter.convert(content, message_settings)  # ty:ignore[invalid-argument-type]

    async def _send_message(self, ditto_message: DittoMessage) -> None:
        if not self._sender:
            return

        for envelope in ditto_message:
            await self._sender.send(envelope.model_dump_json().encode())

    async def _sender_loop(self) -> None:
        while True:
            msg = await self._send_queue.get()
            await self._send_message(msg)

    async def _handle_vehicle_message(self, vehicle_message: VehicleMessage) -> None:
        for formatter_backend in vehicle_message.message_settings.allowed_ditto_formats:
            formatter = self._envelope_formatters.get(formatter_backend)
            if not formatter:
                continue
            ditto_message = await formatter.format(vehicle_message)
            logger.trace("Ditto message: {}", ditto_message)
            await self._send_queue.put(ditto_message)

    async def _clear_loop(self):
        logger.info("Clear loop starting")
        sources = {
            ms.source_name for c in settings.consumers for ms in c.message_settings
        }
        while True:
            for formatter in self._envelope_formatters.values():
                await self._send_queue.put(await formatter.delete_all(list(sources)))

            logger.info("Clear complete")
            await asyncio.sleep(settings.clear_loop_interval_s)

    async def run(self) -> None:
        async with self._resources():
            if self._toll_loader and self._sender:
                await self._toll_loader.load(self._sender)

            logger.info("Service running")
            try:
                async for message in self._messages():
                    logger.trace("Queue Length: {}", self._message_queue.qsize())
                    logger.info(
                        "Message received from sensor {source_name}, on topic {topic}",
                        source_name=message.message_settings.source_name,
                        topic=message.message_settings.topic,
                    )
                    if not message.message_settings.enabled:
                        logger.debug("Received message is not enabled")
                        continue

                    vehicle_message = self._convert_message(message)
                    if vehicle_message is None:
                        logger.trace("Vehicle message is None")
                        continue
                    logger.trace("Vehicle message: {}", vehicle_message)
                    await self._handle_vehicle_message(vehicle_message)
            except (KeyboardInterrupt, asyncio.CancelledError):
                logger.info("Timeout loop stopped")
                logger.info("Stopping bridge service...")
