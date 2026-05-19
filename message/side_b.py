""" Side B for the chat application """
from config import QUEUE_TO_A, QUEUE_TO_B
from utils import start_chat


if __name__ == "__main__":
    try:
        # Start the chat application for side B
        start_chat(
            side_name="B",
            prompt="B",
            send_queue=QUEUE_TO_A,
            receive_queue=QUEUE_TO_B,
            from_side="A",
            to_side="A",
        )
    except KeyboardInterrupt:
        print("\nExiting side B.")
