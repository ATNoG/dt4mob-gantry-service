import asyncio
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request
from loguru import logger

from app.drivers.consumer import ConsumerMessage
from app.interface.consumer import ConsumerInterface
from app.settings.consumer import WebhookConsumerSettings


class WebhookConsumerInterface(ConsumerInterface):
    def __init__(
        self,
        *,
        advanced_settings: WebhookConsumerSettings,
        queue: asyncio.Queue[ConsumerMessage],
    ) -> None:
        super().__init__(advanced_settings=advanced_settings)
        self.settings = advanced_settings
        self.queue = queue
        self.app = FastAPI()

        @self.app.post("/{topic:path}", status_code=HTTPStatus.NO_CONTENT)
        async def _(request: Request, topic: str) -> None:
            if topic not in self.message_settings:
                return

            body = await request.body()

            logger.debug("Received message from: {topic}", topic=topic)
            logger.debug("Content: {content}", content=body)

            message_config = self.message_settings[topic]

            await self.queue.put(
                ConsumerMessage(
                    message_settings=message_config,
                    content=body,
                )
            )
            logger.trace("Queue: {}", self.queue)

    async def loop(self) -> None:
        logger.info("Starting Webhook consumer")
        config = uvicorn.Config(
            self.app, host=self.settings.host, port=self.settings.port
        )
        server = uvicorn.Server(config)
        await server.serve()
