import asyncio
import logging
from typing import Any

from .errors import ConnectionCloseError
from .reader import Reader


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Connection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = Reader(reader)
        self._writer = writer

    async def get(self) -> Any:
        ...

    async def send(self, data: bytes):
        ...

    async def close(self):
        try:
            self._writer.close()
            await self._writer.wait_closed()
        except Exception as exc:
            logger.exception("Connection close error")
            raise ConnectionCloseError(exc) from exc
        else:
            logger.info("Connection closed")
