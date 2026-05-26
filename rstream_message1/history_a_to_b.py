"""Read saved A -> B message history from the stream."""

import asyncio

from rstream import (
    AMQPMessage,
    Consumer,
    ConsumerOffsetSpecification,
    OffsetType,
    amqp_decoder,
)

from config import HOST, PASSWORD, STREAM_A_TO_B, STREAM_PORT, USERNAME


async def on_message(message: AMQPMessage, message_context):
    print("A -> B history:", message.body.decode())


async def main():
    consumer = Consumer(
        host=HOST,
        port=STREAM_PORT,
        username=USERNAME,
        password=PASSWORD,
    )
    await consumer.start()

    await consumer.subscribe(
        stream=STREAM_A_TO_B,
        callback=on_message,
        decoder=amqp_decoder,
        offset_specification=ConsumerOffsetSpecification(OffsetType.FIRST),
    )

    try:
        await asyncio.Future()
    finally:
        await consumer.close()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nInterrupted")
