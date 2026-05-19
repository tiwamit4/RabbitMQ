""" This script emits log messages to a direct exchange named 'direct_logs'. 
The messages are sent to queues that are bound to the exchange with a specific routing key. 
The routing key is determined by the first command-line argument, 
which represents the severity of the log message (e.g., 'info', 'warning', 'error').
The message body is constructed from the remaining command-line arguments, or defaults to 'Hello World!' 
if no additional arguments are provided. """


import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

try:
    while True:
        severity = input("Enter severity [info/warning/error]: ").strip() or "info"
        if severity.lower() in {"exit", "quit"}:
            break

        message = input("Enter message: ").strip() or "Hello World!"
        if message.lower() in {"exit", "quit"}:
            break

        channel.basic_publish(
            exchange='direct_logs', routing_key=severity, body=message)
        print(f" [x] Sent {severity}:{message}")
except KeyboardInterrupt:
    print("Interrupted")
finally:
    connection.close()
