"""RPC client for the message app.

Type a message. The client sends it to the server and waits for the server's
response using RabbitMQ's reply_to and correlation_id pattern.
"""
import uuid

import pika

from config import EXIT_WORDS, HOST, RPC_QUEUE


class MessageRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST)
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.response = None
        self.correlation_id = None

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body):
        if props.correlation_id == self.correlation_id:
            self.response = body.decode()

    def call(self, message):
        self.response = None
        self.correlation_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange="",
            routing_key=RPC_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=message,
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=None)

        return self.response

    def close(self):
        self.connection.close()


def main():
    client = MessageRpcClient()
    print("Message RPC client started.")
    print("Type a message and press Enter. Type exit or quit to stop.")

    try:
        while True:
            message = input("client> ").strip()
            if message.lower() in EXIT_WORDS:
                break
            if not message:
                continue

            print(f" [x] Sending request: {message}")
            response = client.call(message)
            print(f" [.] Response: {response}")
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        client.close()


if __name__ == "__main__":
    main()
