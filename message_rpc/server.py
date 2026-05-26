"""RPC server for the message app.

Run this file first. It waits for message requests and sends a response back
to the client's private callback queue.
"""
import pika
from config import HOST, RPC_QUEUE


def build_response(message):
    return f"Server received: {message}"


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RPC_QUEUE)
    channel.basic_qos(prefetch_count=1)

    def on_request(ch, method, props, body):
        message = body.decode()
        print(f" [.] Received request: {message}")

        response = build_response(message)
        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id,
            ),
            body=response,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f" [x] Sent response: {response}")

    channel.basic_consume(queue=RPC_QUEUE, on_message_callback=on_request)
    print(" [x] Awaiting RPC message requests. To exit press CTRL+C")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
