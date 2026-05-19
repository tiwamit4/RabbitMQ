#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare a durable queue with quorum type
# Note: Quorum queues are a type of durable queue that provide high availability and data safety
channel.queue_declare(queue='hello', durable=True, arguments={'x-queue-type': 'quorum'})

# Publish a message to the 'hello' queue
# The exchange parameter is set to an empty string, which means that the message will be sent directly to the queue specified by the routing_key parameter.
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()