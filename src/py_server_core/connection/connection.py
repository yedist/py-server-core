import asyncio
import logging
from typing import Any, Self, Optional

from .errors import ConnectionCloseError
from .reader import Reader


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Connection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = Reader(reader)
        self._writer = writer

    @classmethod
    async def connect(cls, host: str, port: int, timeout: Optional[float] = None) -> Self:  # need try and need test
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        return cls(reader, writer)

    async def get(self) -> Any:
        ...

    async def send(self, data: bytes):
        self._writer.write(data)
        await self._writer.drain()

    async def close(self):
        try:
            self._writer.close()
            await self._writer.wait_closed()
        except Exception as exc:
            logger.exception("Connection close error")
            raise ConnectionCloseError(exc) from exc
        else:
            logger.info("Connection closed")
