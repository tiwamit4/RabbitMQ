"""Shared helpers for hybrid messaging with RabbitMQ queues and streams.

Queues are used for live delivery. Streams are used as message history.
"""

import asyncio
import threading

import pika
from rstream import AMQPMessage, Producer

from config import EXIT_WORDS, HOST, PASSWORD, STREAM_PORT, USERNAME


def create_queue_channel(*queues):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    for queue in queues:
        channel.queue_declare(queue=queue, durable=True)
    return connection, channel


def receive_live_messages(receive_queue, from_side, prompt):
    connection, channel = create_queue_channel(receive_queue)

    def callback(ch, method, properties, body):
        print(f"\n{from_side}: {body.decode()}")
        print(f"{prompt}> ", end="", flush=True)

    channel.basic_consume(
        queue=receive_queue,
        on_message_callback=callback,
        auto_ack=True,
    )

    try:
        channel.start_consuming()
    finally:
        connection.close()


def make_stream_producer():
    return Producer(
        host=HOST,
        port=STREAM_PORT,
        username=USERNAME,
        password=PASSWORD,
    )


async def create_streams(*streams):
    producer = make_stream_producer()
    await producer.start()
    try:
        for stream in streams:
            await producer.create_stream(stream, exists_ok=True)
    finally:
        await producer.close()


async def publish_hybrid_message(queue_channel, stream_producer, queue, stream, text):
    queue_channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=text,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )

    stream_message = AMQPMessage(body=text.encode())
    await stream_producer.send_wait(stream, stream_message)


async def send_messages(send_queue, history_stream, side_name, to_side, prompt):
    queue_connection, queue_channel = create_queue_channel(send_queue)
    stream_producer = make_stream_producer()
    await stream_producer.start()

    print(f"Side {side_name} started.")
    print("Live messages go to queue; history is saved to stream.")
    print("Type exit or quit to stop.")

    try:
        while True:
            text = await asyncio.to_thread(input, f"{prompt}> ")
            text = text.strip()

            if text.lower() in EXIT_WORDS:
                break
            if not text:
                continue

            await publish_hybrid_message(
                queue_channel,
                stream_producer,
                send_queue,
                history_stream,
                text,
            )
            print(f"sent to {to_side}: {text}")
    finally:
        await stream_producer.close()
        queue_connection.close()


async def start_side(
    side_name,
    prompt,
    send_queue,
    receive_queue,
    send_stream,
    receive_stream,
    from_side,
    to_side,
):
    create_queue_channel(send_queue, receive_queue)[0].close()
    await create_streams(send_stream, receive_stream)

    receiver_thread = threading.Thread(
        target=receive_live_messages,
        args=(receive_queue, from_side, prompt),
        daemon=True,
    )
    receiver_thread.start()

    await send_messages(send_queue, send_stream, side_name, to_side, prompt)
