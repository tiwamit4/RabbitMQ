""" 
This is a simple example of a RabbitMQ producer that sends messages to a queue.
The producer will send a message every second, and the message will contain a counter that increments with each message. 
The messages are marked as persistent, so they will survive a RabbitMQ server restart."""

import pika
import sys,time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True, arguments={'x-queue-type': 'quorum'})

message = ' '.join(sys.argv[1:]) or "Hello World!"

i = 10
while True:
    i += 1
    channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=f"{message} {i}",
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))
    print(f" [x] Sent {message} {i}")
    time.sleep(1)

connection.close()