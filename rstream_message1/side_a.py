"""Side A for the hybrid queue + stream message app."""

import asyncio

from config import QUEUE_A_TO_B, QUEUE_B_TO_A, STREAM_A_TO_B, STREAM_B_TO_A
from utils import start_side


async def main():
    await start_side(
        side_name="A",
        prompt="A",
        send_queue=QUEUE_A_TO_B,
        receive_queue=QUEUE_B_TO_A,
        send_stream=STREAM_A_TO_B,
        receive_stream=STREAM_B_TO_A,
        from_side="B",
        to_side="B",
    )


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nInterrupted")
