import asyncio
import logging

from .errors import ServerStartError, ServerCloseError


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Server:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._server: asyncio.Server | None = None

    @property
    def is_running(self) -> bool:
        return self._server is not None

    async def _on_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        pass

    async def up(self):
        if self.is_running:
            return

        try:
            self._server = await asyncio.start_server(self._on_connection, self._host, self._port)
        except Exception as exc:
            logger.exception("Server up error")
            raise ServerStartError(exc) from exc
        else:
            addresses = [
                (sock.family, sock.getsockname())
                for sock in (self._server.sockets or [])
            ]
            logger.info("Server up", extra={"addresses": addresses})

    async def close(self):
        if not self.is_running:
            return

        try:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
        except Exception as exc:
            logger.exception("Server close error")
            raise ServerCloseError(exc) from exc
        else:
            logger.info("Server closed")
