"""Configuration for the hybrid RabbitMQ queue + stream message app."""

HOST = "localhost"
STREAM_PORT = 5552
USERNAME = "guest"
PASSWORD = "guest"

QUEUE_A_TO_B = "hybrid-queue-a-to-b"
QUEUE_B_TO_A = "hybrid-queue-b-to-a"

STREAM_A_TO_B = "hybrid-stream-a-to-b"
STREAM_B_TO_A = "hybrid-stream-b-to-a"

EXIT_WORDS = {"exit", "quit"}
