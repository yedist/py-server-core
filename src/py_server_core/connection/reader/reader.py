class Reader:
    def __init__(self, reader: asyncio.StreamReader):
        self._reader = reader
