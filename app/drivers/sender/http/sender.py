import ssl
from typing import Optional

import httpx
from loguru import logger

from app.interface.sender import SenderInterface
from app.settings.sender import HTTPSenderSettings


class HTTPSenderInterface(SenderInterface):
    def __init__(self, http_settings: HTTPSenderSettings) -> None:
        auth: Optional[httpx.Auth] = None
        if http_settings.username and http_settings.password:
            auth = httpx.BasicAuth(
                username=http_settings.username,
                password=http_settings.password,
            )
        ctx = ssl.create_default_context(cafile=http_settings.cafile)
        if http_settings.client_crt:
            ctx.load_cert_chain(
                certfile=http_settings.client_crt, keyfile=http_settings.client_key
            )
        self.httpx_client = httpx.AsyncClient(
            base_url=http_settings.get_url(),
            verify=ctx,
            auth=auth,
        )

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def send(self, payload: bytes) -> None:
        logger.debug("Sending: {payload}", payload=payload)
        try:
            res = await self.httpx_client.post(
                "", headers={"content-type": "application/json"}, content=payload
            )
            logger.trace("Response {res}", res=res)
        except Exception as e:
            logger.error("HTTP Sender failed to send: {err}", err=repr(e))
