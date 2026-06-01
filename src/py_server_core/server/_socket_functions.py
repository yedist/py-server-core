from typing import Iterable
import socket


def get_addresses(sockets: Iterable[socket.socket] | None) -> list[tuple[socket.AddressFamily, object]]:
    sockets = sockets or []

    return [
        (sock.family, sock.getsockname())
        for sock in sockets
    ]
