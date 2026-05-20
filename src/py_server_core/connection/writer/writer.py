import asyncio

from .errors import WriterError


class Writer:
    def __init__(self, output_stream: asyncio.StreamWriter):
        self.output_stream = output_stream

    async def write(self, data):
        try:
            self.output_stream.write(data)
            await self.output_stream.drain()
        except Exception as exc:
            raise WriterError(exc) from exc
