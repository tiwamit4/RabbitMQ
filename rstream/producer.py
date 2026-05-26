import asyncio
from rstream import Producer, AMQPMessage

STREAM = "hello-stream"

async def main():
    producer = Producer(
        host="localhost",
        port=5552,
        username="guest",
        password="guest",
    )

    await producer.start()

    await producer.create_stream(STREAM, exists_ok=True)
    
    for i in range(10):
        msg = AMQPMessage(
            body=f"message-{i}".encode()
        )
        await producer.send(STREAM, msg)
        print("sent:", i)

    await producer.close()

asyncio.run(main())