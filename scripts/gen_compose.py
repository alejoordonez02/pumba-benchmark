from cfg import BANDWIDTH_MBYTESPS, MSG_SIZE_BYTES, RUNS, SERVER_PORT


def gen_compose(server_port: int, msg_size_bytes: int, bandwidth_mbps: int, runs: int):
    return f"""\
services:
  pumba:
    image: gaiaadm/pumba
    container_name: pumba
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: netem --duration 5m rate --rate {bandwidth_mbps}mbit 're2:.*sender.*|.*receiver.*'
    depends_on:
      - sender

  sender:
    build:
      dockerfile: sender/Dockerfile
    container_name: sender
    environment:
      - SERVER_ADDR=receiver:{server_port}
      - MSG_SIZE_BYTES={msg_size_bytes}
      - RUNS={runs}
    depends_on:
      - receiver

  receiver:
    build:
      dockerfile: receiver/Dockerfile
    container_name: receiver
    environment:
      - SERVER_ADDR=0.0.0.0:{server_port}
      - MSG_SIZE_BYTES={msg_size_bytes}
      - RUNS={runs}
"""


def main():
    bandwidth_mbps = BANDWIDTH_MBYTESPS * 8
    compose = gen_compose(SERVER_PORT, MSG_SIZE_BYTES, bandwidth_mbps, RUNS)
    with open("compose.yaml", "w") as f:
        f.write(compose)


if __name__ == "__main__":
    main()
