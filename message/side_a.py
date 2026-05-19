""" Side A for the chat application """
from config import QUEUE_TO_A, QUEUE_TO_B
from utils import start_chat


if __name__ == "__main__":
    try:
        start_chat(
            side_name="A",
            prompt="A",
            send_queue=QUEUE_TO_B,
            receive_queue=QUEUE_TO_A,
            from_side="B",
            to_side="B",
        )
    except KeyboardInterrupt:
        print("\nExiting side A.")
