import asyncio


class Writer:
    def __init__(self, output_stream: asyncio.StreamWriter):
        self.output_stream = output_stream

    async def write(self, data):
        self.output_stream.write(data)
        await self.output_stream.drain()
