import asyncio
from rstream import (
    AMQPMessage,
    Consumer,
    ConsumerOffsetSpecification,
    OffsetType,
    amqp_decoder,
)

STREAM = "hello-stream1"

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
        #NEXT IS USED TO RECEIVE ONLY MESSAGES SENT AFTER THE SUBSCRIPTION, NOT INCLUDING THOSE SENT BEFORE THE SUBSCRIPTION
        # offset_specification=ConsumerOffsetSpecification(OffsetType.NEXT), 
        # FIRST IS USED TO RECEIVE ALL MESSAGES IN THE STREAM, INCLUDING THOSE SENT BEFORE THE SUBSCRIPTION
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