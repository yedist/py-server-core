import asyncio
import logging
from typing import Any, Self, Optional

from .errors import ConnectionCloseError, ConnectError
from .reader import Reader
from .writer import Writer


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Connection:
    def __init__(self, input_stream: asyncio.StreamReader, output_stream: asyncio.StreamWriter):
        self.reader = Reader(input_stream)
        self.writer = Writer(output_stream)

    @classmethod
    async def connect(cls, host: str, port: int, timeout: Optional[float] = None) -> Self:  # need try and need test
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        except Exception as exc:
            logger.exception("Connection attempt failed")
            raise ConnectError(exc) from exc

        return cls(reader, writer)

    async def get(self) -> Any:
        ...

    async def send(self, data: bytes):
        await self.writer.write(data)

    async def close(self):
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except Exception as exc:
            logger.exception("Connection close error")
            raise ConnectionCloseError(exc) from exc
        else:
            logger.info("Connection closed")
