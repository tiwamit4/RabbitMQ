# Hybrid RabbitMQ Queue + Stream Message App

This app uses both RabbitMQ queues and RabbitMQ Streams.

- Queues are used for live delivery.
- Streams are used to save message history.
- Every message is published to both a queue and a stream.
- Queues are durable, and queue messages are marked persistent.

Flow from A to B:

```text
A input
  |---> queue: hybrid-queue-a-to-b   ---> B receives live
  '---> stream: hybrid-stream-a-to-b ---> saved as history
```

Flow from B to A:

```text
B input
  |---> queue: hybrid-queue-b-to-a   ---> A receives live
  '---> stream: hybrid-stream-b-to-a ---> saved as history
```

Run RabbitMQ with normal AMQP and stream plugin enabled.

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

Read A to B history:

```bash
python3 history_a_to_b.py
```

Read B to A history:

```bash
python3 history_b_to_a.py
```

Type `exit` or `quit` to stop a side.
