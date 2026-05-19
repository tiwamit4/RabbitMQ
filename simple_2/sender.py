## emit logs
""" This script emits log messages to a fanout exchange named 'logs'. 
The messages are sent to all queues that are bound to the exchange. 
"""

#!/usr/bin/env python
import pika

# establish connection to RabbitMQ server and create a channel
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare a fanout exchange named 'logs'
channel.exchange_declare(exchange='logs', exchange_type='fanout')

try:
    while True:
        message = input("Enter message: ").strip()
        if message.lower() in {"exit", "quit"}:
            break
        message = message or "info: Hello World!"
        # publish the message to the 'logs' exchange with an empty routing key
        channel.basic_publish(exchange='logs', routing_key='', body=message)
        print(f" [x] Sent {message}")
except KeyboardInterrupt:
    print("Interrupted")
finally:
    connection.close()
