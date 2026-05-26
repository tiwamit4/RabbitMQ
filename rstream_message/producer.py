import asyncio
from rstream import Producer, AMQPMessage

STREAM = "hello-stream2"

async def main():
    producer = Producer(
        host="localhost",
        port=5552,
        username="guest",
        password="guest",
    )

    await producer.start()

    await producer.create_stream(STREAM, exists_ok=True)

    try:
        while True:
            text = input("message: ").strip()

            if text.lower() in {"exit", "quit"}:
                break

            if not text:
                continue

            msg = AMQPMessage(
                body=text.encode()
            )

            await producer.send_wait(STREAM, msg)
            print("sent:", msg.body.decode())

    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        await producer.close()

asyncio.run(main())