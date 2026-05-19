"""
Topic exchange example.
Run the receiver first:
"""
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

try:
    while True:
        # routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
        routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

        message = input("enter message: ")

        # message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=message)
        print(f" [x] Sent {routing_key}:{message}")
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    connection.close()