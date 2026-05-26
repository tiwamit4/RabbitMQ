"""Shared helpers for two-side messaging with RabbitMQ Streams."""

import asyncio

from rstream import (
    AMQPMessage,
    Consumer,
    ConsumerOffsetSpecification,
    OffsetType,
    Producer,
    amqp_decoder,
)

from config import EXIT_WORDS, HOST, PASSWORD, PORT, USERNAME


def make_producer():
    return Producer(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
    )


def make_consumer():
    return Consumer(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
    )


async def create_streams(*streams):
    producer = make_producer()
    await producer.start()
    try:
        for stream in streams:
            await producer.create_stream(stream, exists_ok=True)
    finally:
        await producer.close()


async def consume_messages(stream, from_side, prompt):
    consumer = make_consumer()
    await consumer.start()

    async def on_message(message: AMQPMessage, message_context):
        print(f"\n{from_side}: {message.body.decode()}")
        print(f"{prompt}> ", end="", flush=True)

    await consumer.subscribe(
        stream=stream,
        callback=on_message,
        decoder=amqp_decoder,
        offset_specification=ConsumerOffsetSpecification(OffsetType.NEXT),
    )

    try:
        await asyncio.Future()
    finally:
        await consumer.close()


async def send_messages(stream, side_name, to_side, prompt):
    producer = make_producer()
    await producer.start()

    print(f"Side {side_name} started. Type a message and press Enter.")
    print("Type exit or quit to stop.")

    try:
        while True:
            text = await asyncio.to_thread(input, f"{prompt}> ")
            text = text.strip()

            if text.lower() in EXIT_WORDS:
                break
            if not text:
                continue

            message = AMQPMessage(body=text.encode())
            await producer.send_wait(stream, message)
            print(f"sent to {to_side}: {text}")
    finally:
        await producer.close()


async def start_side(side_name, prompt, send_stream, receive_stream, from_side, to_side):
    await create_streams(send_stream, receive_stream)

    consumer_task = asyncio.create_task(
        consume_messages(receive_stream, from_side, prompt)
    )

    try:
        await send_messages(send_stream, side_name, to_side, prompt)
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
