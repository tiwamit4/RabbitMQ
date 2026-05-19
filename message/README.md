# Simple RabbitMQ Message App

This folder has a tiny two-side message app:

- `side_a.py` sends messages to B and receives messages from B.
- `side_b.py` sends messages to A and receives messages from A.
- `config.py` contains queue names, host, and exit words.
- `utils.py` contains the shared RabbitMQ connection, send, and receive code.

Run RabbitMQ first, then open two terminals.

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/message
python3 side_a.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/message
python3 side_b.py
```

Type a message in either terminal and press Enter.

Type `exit` or `quit` to stop that side.
