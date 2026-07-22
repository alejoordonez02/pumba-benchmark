import os
from datetime import datetime
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket


class Receiver:
    def __init__(self, host_addr: tuple[str, int], send_size_bytes: int, runs: int):
        self._host_addr = host_addr
        self._recv_size_bytes = send_size_bytes
        self._runs = runs

    def start(self) -> float:
        """
        Returns the average time it took to receive each message.
        """
        listener = socket(AF_INET, SOCK_STREAM)
        listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        listener.bind(self._host_addr)
        listener.listen()
        skt, _ = listener.accept()

        start = datetime.now()
        for _ in range(0, self._runs):
            recvd = 0
            while recvd < self._recv_size_bytes:
                recvd += len(skt.recv(self._recv_size_bytes - recvd))
        skt.sendall(b"ACK")

        end = datetime.now()

        skt.close()
        listener.close()

        total_elapsed = end.timestamp() - start.timestamp()
        avg_elapsed = total_elapsed / self._runs

        return avg_elapsed


DEFAULT_SERVER_ADDR = "0.0.0.0:1234"


def main():
    peer_addr_str = os.getenv("SERVER_ADDR", DEFAULT_SERVER_ADDR).split(":")
    host_addr = (peer_addr_str[0], int(peer_addr_str[1]))
    recv_size_bytes = int(os.environ["MSG_SIZE_BYTES"])
    runs = int(os.environ["RUNS"])

    receiver = Receiver(host_addr, recv_size_bytes, runs)
    avg_elapsed = receiver.start()

    print(f"avg_elapsed={avg_elapsed}")

    exit(0)


if __name__ == "__main__":
    main()
