# RabbitMQ Message RPC App

This is a simple messaging app using RabbitMQ RPC.

- `server.py` receives a message request and sends a response.
- `client.py` lets you type messages and waits for the server response.
- `config.py` contains the RabbitMQ host and queue name.

Run RabbitMQ first.

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/message_rpc
python3 server.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/message_rpc
python3 client.py
```

Example:

```text
client> hello server
 [x] Sending request: hello server
 [.] Response: Server received: hello server
```

Type `exit` or `quit` to stop the client.
