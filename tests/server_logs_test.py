import asyncio
import logging
import socket

from src.py_server_core import Server
from test_tools import test_log_queue


def initial():
    logs_queue, log_handler = test_log_queue()

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(log_handler)

    server = Server(
        host="127.0.0.1",
        port=0,  # == the system will select a free port
    )

    return server, logs_queue


async def main():
    server, logs_queue = initial()

    await server.up()
    await server.close()

    up_log, close_log = logs_queue.get(), logs_queue.get()

    # ['level'] test:
    assert up_log.levelno == close_log.levelno == logging.INFO

    # ['event'] test:
    assert up_log.message == "Server up"
    assert close_log.message == "Server closed"

    # content test (up_log):
    assert len(up_log.addresses) == 1
    family, address = up_log.addresses[0]

    assert family == socket.AF_INET  # IPv4 ('127.0.0.1' is IPv4)
    host, port = address  # this is an IPv4 address structure.

    assert host == "127.0.0.1"
    assert 0 < port


if __name__ == '__main__':
    asyncio.run(main())
