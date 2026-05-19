import asyncio
from typing import Any

from .errors import ConnectionCloseError


class Connection:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
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
            raise ConnectionCloseError(exc) from exc
