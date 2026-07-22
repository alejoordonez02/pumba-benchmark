import os
import random
import string
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, socket
from time import sleep


class Sender:
    def __init__(self, peer_addr: tuple[str, int], send_size_bytes: int, runs: int):
        self._peer_addr = peer_addr
        self._send_size_bytes = send_size_bytes
        self._runs = runs

    def start(self) -> float:
        """
        Returns the average time it took to perform the send.
        """
        skt = socket(AF_INET, SOCK_STREAM)
        skt.connect(self._peer_addr)

        msg = "".join(
            random.choices(string.ascii_lowercase, k=self._send_size_bytes)
        ).encode()

        start = datetime.now()
        for _ in range(0, self._runs):
            skt.sendall(msg)
        skt.recv(len(b"ACK"))

        end = datetime.now()

        skt.close()

        total_elapsed = end.timestamp() - start.timestamp()
        avg_elapsed = total_elapsed / self._runs

        return avg_elapsed


DEFAULT_SERVER_ADDR = "localhost:1234"
SERVER_WAIT_TIME = 3


def main():
    peer_addr_str = os.getenv("SERVER_ADDR", DEFAULT_SERVER_ADDR).split(":")
    peer_addr = (peer_addr_str[0], int(peer_addr_str[1]))
    send_size_bytes = int(os.environ["MSG_SIZE_BYTES"])
    runs = int(os.environ["RUNS"])

    sender = Sender(peer_addr, send_size_bytes, runs)

    sleep(SERVER_WAIT_TIME)  # wait for server
    avg_elapsed = sender.start()

    print(f"avg_elapsed={avg_elapsed}")

    exit(0)


if __name__ == "__main__":
    main()
