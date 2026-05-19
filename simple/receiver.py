#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare a durable queue with quorum type
    # Note: Quorum queues are a type of durable queue that provide high availability and data safety.
    channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

    # Define a callback function to process received messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
    
    # Start consuming messages from the 'hello' queue
    # The auto_ack=True parameter means that the message will be acknowledged automatically after the callback function is executed.
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)