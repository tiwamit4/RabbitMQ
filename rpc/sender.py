"""RPC Server

To run this example, first start the server (this script) and then run the client (client.py).
"""
import pika

# connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# create a channel
channel = connection.channel()

# declare a queue for receiving requests. The queue is durable, meaning it will survive a RabbitMQ server restart, 
# and it is a quorum queue, which provides better reliability and consistency guarantees.
channel.queue_declare(queue='rpc_queue', durable=True, arguments={'x-queue-type': 'quorum'})

# This tells RabbitMQ not to give more than one message to a worker at a time. 
# Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one. 
# Instead, it will dispatch it to the next worker that is not still busy.
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# This is the callback function that will be called when a request is received. It will compute the Fibonacci number and send the response back to the client.
def on_request(ch, method, props, body):
    n = int(body)

    print(f" [.] fib({n})")
    response = fib(n)
    print(f" [.] fib({n}) = {response}")

    # Send the response back to the client using the reply_to and correlation_id properties of the request message.
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    
    # Acknowledge the request message to RabbitMQ, indicating that it has been processed and 
    # can be removed from the queue.
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
except KeyboardInterrupt:
    pass
finally:
    connection.close()

# fibonacci_rpc = FibonacciRpcClient()

# print(" [x] Requesting fib(30)")
# response = fibonacci_rpc.call(30)
# print(f" [.] Got {response}")

