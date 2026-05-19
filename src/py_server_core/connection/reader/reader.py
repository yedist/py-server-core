import asyncio
from typing import Optional

from .errors import ReadError


class Reader:
    def __init__(self, reader: asyncio.StreamReader):
        self._reader = reader

    async def read_to(self, size: int, timeout: Optional[float] = None) -> bytes:
        if not isinstance(size, int):
            raise TypeError("size must be an integer")
        if size <= 0:
            raise ValueError("size must be positive")

        try:
            data = await asyncio.wait_for(self._reader.read(size), timeout)
        except Exception as exc:
            raise ReadError(exc) from exc

        if data == b'':
            raise EOFError()

        return data

    async def read_exactly(self, size: int, timeout: Optional[float] = None) -> bytes:
        if not isinstance(size, int):
            raise TypeError("size must be an integer")

        try:
            return await asyncio.wait_for(self._reader.readexactly(size), timeout)
        except Exception as exc:
            raise ReadError(exc) from exc

    async def read_until(self, until: bytes | bytearray | memoryview, timeout: Optional[float] = None) -> bytes:
        if not isinstance(until, (bytes, bytearray, memoryview)):
            raise TypeError("until should be bytes-like object")

        try:
            return await asyncio.wait_for(self._reader.readuntil(until), timeout)
        except Exception as exc:
            raise ReadError(exc) from exc

    async def read_forever(self) -> bytes:
        try:
            return await self._reader.read(-1)
        except Exception as exc:
            raise ReadError(exc) from exc
