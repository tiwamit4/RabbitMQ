"""RPC Server

To run this example, first start the server (this script) and then run the client (client.py).
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue', durable=True, arguments={'x-queue-type': 'quorum'})

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(f" [.] fib({n})")
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
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

