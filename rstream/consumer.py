import asyncio
from rstream import (
    AMQPMessage,
    Consumer,
    ConsumerOffsetSpecification,
    OffsetType,
    amqp_decoder,
)

STREAM = "hello-stream"

async def on_message(message: AMQPMessage, message_context):
    print("received:", message.body.decode())

async def main():
    consumer = Consumer(
        host="localhost",
        port=5552,
        username="guest",
        password="guest",
    )

    await consumer.start()

    await consumer.subscribe(
        stream=STREAM,
        callback=on_message,
        decoder=amqp_decoder,
        offset_specification=ConsumerOffsetSpecification(OffsetType.FIRST),
    )

    await asyncio.Future()

asyncio.run(main())