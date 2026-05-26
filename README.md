# RabbitMQ Examples Execution Order

This folder contains small RabbitMQ examples arranged from basic queue usage to streams and hybrid queue + stream messaging.

## Setup

Install dependencies:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq
python3 -m pip install -r requirements.txt
```

Start RabbitMQ normally:

```bash
sudo systemctl start rabbitmq-server
```

For stream examples, enable RabbitMQ Streams:

```bash
sudo rabbitmq-plugins enable rabbitmq_stream rabbitmq_stream_management
sudo systemctl restart rabbitmq-server
```

Check ports:

```bash
ss -ltnp | grep -E '5672|5552|15672'
```

- `5672` is used by normal queue/exchange/RPC examples with `pika`.
- `5552` is used by RabbitMQ Stream examples with `rstream`.
- `15672` is the management UI if enabled.

## Recommended Order

### 1. Simple Queue

Folder: `simple`

Concepts:

- producer sends one message
- consumer receives from one queue
- default exchange
- quorum durable queue

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple
python3 receiver.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple
python3 sender.py
```

### 2. Work Queue

Folder: `simple_1`

Concepts:

- persistent task messages
- manual acknowledgement
- `basic_qos(prefetch_count=1)`
- multiple workers can share work

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_1
python3 receiver.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_1
python3 sender.py "task..."
```

Optional: run another receiver in Terminal 3 to see work distributed.

### 3. Fanout Exchange

Folder: `simple_2`

Concepts:

- broadcast messages
- temporary exclusive queues
- every receiver gets the same message

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_2
python3 receiver.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_2
python3 receiver.py
```

Terminal 3:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_2
python3 sender.py
```

### 4. Direct Exchange

Folder: `simple_3`

Concepts:

- routing by exact severity
- `info`, `warning`, `error`

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_3
python3 receiver.py error
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_3
python3 receiver.py info warning
```

Terminal 3:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple_3
python3 sender.py
```

### 5. Topic Exchange

Folder: `simple4`

Concepts:

- routing by pattern
- `*` matches one word
- `#` matches zero or more words

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple4
python3 receiver.py "*.critical"
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple4
python3 receiver.py "#"
```

Terminal 3:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/simple4
python3 sender.py kern.critical
```

### 6. Two-Side Queue Message App

Folder: `message`

Concepts:

- A and B can both send and receive
- two queues are used, one for each direction
- shared `utils.py` and `config.py`

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

### 7. RPC Fibonacci Example

Folder: `rpc`

Concepts:

- request queue
- callback reply queue
- `reply_to`
- `correlation_id`

Note: in this folder, `sender.py` is the RPC server and `receiver.py` is the RPC client.

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rpc
python3 sender.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rpc
python3 receiver.py
```

### 8. Message RPC App

Folder: `message_rpc`

Concepts:

- client sends text request
- server returns response
- same RPC pattern as the Fibonacci example, but easier to read

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

### 9. Basic RabbitMQ Stream

Folder: `rstream`

Concepts:

- RabbitMQ Streams
- stream port `5552`
- producer creates stream and sends messages
- consumer reads from stream

Run producer first to create and fill the stream:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream
python3 producer.py
```

Then run consumer:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream
python3 consumer.py
```

### 10. Interactive RabbitMQ Stream

Folder: `rstream_1`

Concepts:

- interactive producer
- stream consumer
- offset behavior with `FIRST` and `NEXT`

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream_1
python3 consumer.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream_1
python3 producer.py
```

### 11. Two-Side Stream Message App

Folder: `rstream_message`

Concepts:

- A and B can both send and receive
- two streams are used, one for each direction
- streams replace queues

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

### 12. Hybrid Queue + Stream Message App

Folder: `rstream_message1`

Concepts:

- queues are used for live delivery
- streams are used for history
- each message is sent to both a queue and a stream

Terminal 1:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream_message1
python3 side_a.py
```

Terminal 2:

```bash
cd /home/amitranjan/Public/Code/streaming/rabbitmq/rstream_message1
python3 side_b.py
```

Optional history readers:

```bash
python3 history_a_to_b.py
python3 history_b_to_a.py
```

## Quick Troubleshooting

If normal queue examples fail, check RabbitMQ AMQP port:

```bash
ss -ltnp | grep 5672
```

If stream examples fail, check RabbitMQ Stream port:

```bash
ss -ltnp | grep 5552
```

If `rstream` import fails inside the `rstream` folder, run with your virtual environment Python and make sure `rstream` is installed:

```bash
python3 -m pip install rstream
```

If a topic receiver prints usage, pass a binding key:

```bash
python3 receiver.py "#"
python3 receiver.py "*.critical"
```

If a direct receiver prints usage, pass severities:

```bash
python3 receiver.py info warning error
```
