import asyncio
from typing import Optional

class Reader:
    def __init__(self, reader: asyncio.StreamReader):
        self._reader = reader

    async def read_to(self, size: int, timeout: Optional[float] = None) -> bytes:
        if not isinstance(size, int):
            raise TypeError("size must be an integer")
        if size <= 0:
            raise ValueError("size must be positive")

        data = await asyncio.wait_for(self._reader.read(size), timeout)

        if data == b'':
            raise EOFError()

        return data

    async def read_exactly(self, size: int, timeout: Optional[float] = None) -> bytes:
        if not isinstance(size, int):
            raise TypeError("size must be an integer")

        return await asyncio.wait_for(self._reader.readexactly(size), timeout)

    async def read_until(self, until: bytes | bytearray | memoryview, timeout: Optional[float] = None) -> bytes:
        if not isinstance(until, (bytes, bytearray, memoryview)):
            raise TypeError("until should be bytes-like object")

        return await asyncio.wait_for(self._reader.readuntil(until), timeout)

    async def read_forever(self) -> bytes:
        return await self._reader.read(-1)
