"""Configuration for the RabbitMQ Stream two-side message app."""

HOST = "localhost"
PORT = 5552
USERNAME = "guest"
PASSWORD = "guest"

STREAM_A_TO_B = "stream-a-to-b"
STREAM_B_TO_A = "stream-b-to-a"

EXIT_WORDS = {"exit", "quit"}
