from typing import Iterable, Optional
import socket


def get_addresses(sockets: Optional[Iterable[socket.socket]]):
    sockets = sockets or []

    return [
        (sock.family, sock.getsockname())
        for sock in sockets
    ]
