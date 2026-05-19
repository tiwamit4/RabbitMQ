""" 
This is a simple example of a RabbitMQ consumer that receives messages from a queue and processes them
The consumer will print the message to the console, and then sleep for a number of seconds equal to the number of dots 
in the message.
The consumer will acknowledge the message after processing it, so that RabbitMQ can remove it from the queue.
The consumer will also use the basic_qos method to tell RabbitMQ not to give it more than one message at a time, 
so that it can process messages in order and not get overwhelmed with"""

import pika,sys, os
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True, arguments={'x-queue-type': 'quorum'})
print(' [*] Waiting for messages. To exit press CTRL+C')

# This is the callback function that will be called when a message is received
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

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