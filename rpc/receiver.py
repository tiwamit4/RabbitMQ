"""RPC client that sends a request to the RPC server and waits for the response."""
import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        # Establish a connection to RabbitMQ and create a channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        # create a channel
        self.channel = self.connection.channel()

        # declare a queue for receiving responses. 
        # The queue is exclusive, meaning it will be deleted when the connection is closed.
        result = self.channel.queue_declare(queue='', exclusive=True)

        # get the name of the callback queue
        self.callback_queue = result.method.queue

        # set up a consumer on the callback queue to listen for responses from the server.
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
    
    # This is the callback function that will be called when a response is received from the server. 
    # It checks if the correlation ID of the response matches the correlation ID of the request, 
    # and if so, it stores the response in the self.response variable.
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    # This is the method that sends a request to the server and waits for the response.
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())        # uuid is used to generate a unique correlation ID for each request, which allows the client to match responses to requests.
        
        # Publish the request to the 'rpc_queue' with the appropriate properties, 
        # including the reply_to and correlation_id.
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return int(self.response)



fibonacci_rpc = FibonacciRpcClient()
try:
    while True:
        # print(" [x] Requesting fib(30)")
        # response = fibonacci_rpc.call(30)
        input_value = input("Enter a number: ")
        print(" [x] Requesting fib({})".format(input_value))
        response = fibonacci_rpc.call(int(input_value))
        print(f" [.] Got {response}")
except KeyboardInterrupt:
    pass
finally:
    fibonacci_rpc.connection.close()