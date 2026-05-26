# RabbitMQ Stream Message App

This is a two-side message app using RabbitMQ Streams.

- `side_a.py` sends messages to B and receives messages from B.
- `side_b.py` sends messages to A and receives messages from A.
- `utils.py` contains the shared stream producer and consumer code.
- `config.py` contains the stream names and RabbitMQ connection settings.

Run RabbitMQ with the stream plugin enabled first.

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream_message
python3 side_a.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream_message
python3 side_b.py
```

Type messages in either terminal and press Enter.

Type `exit` or `quit` to stop that side.
