export SERVER_ADDR="0.0.0.0:1234" MSG_SIZE_BYTES="1000000" RUNS="100"

uv run receiver.py &
receiver_pid=$!

trap "kill $receiver_pid 2>/dev/null" EXIT INT TERM

uv run sender.py

pumba netem --duration 5m rate --rate 1mbit re2:^node-.*
