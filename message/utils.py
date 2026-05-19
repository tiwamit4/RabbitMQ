""" Utility functions for RabbitMQ messaging """

""" code description
This module provides utility functions for a simple chat application using RabbitMQ. 
It includes functions to create a connection and channel, receive messages from a queue, send messages to a queue, 
and start the chat application for a given side (A or B). 
The chat application allows two sides to communicate by sending messages through RabbitMQ queues."""

import threading
import pika

from config import EXIT_WORDS, HOST


# Utility functions for RabbitMQ messaging
def create_channel(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST)) # Establish a connection to the RabbitMQ server
    channel = connection.channel()                          # Create a channel for communication
    channel.queue_declare(queue=queue_name)                 # Declare the queue to ensure it exists
    return connection, channel                              # Return the connection and channel for further use

# Function to receive messages from a queue and print them
def receive_messages(receive_queue, from_side, prompt):
    connection, channel = create_channel(receive_queue)     # Create a channel to receive messages from the specified queue

    def callback(ch, method, properties, body):             # Callback function to handle incoming messages
        print(f"\n{from_side}: {body.decode()}")            # Print the received message with the sender's identifier
        print(f"{prompt}> ", end="", flush=True)            # Print the prompt for user input

    # Start consuming messages from the receive queue
    channel.basic_consume(                                  
        queue=receive_queue,                                # Set the queue to consume from
        on_message_callback=callback,                       # Set the callback function to handle incoming messages
        auto_ack=True,                                      # Automatically acknowledge messages after processing
    )

    try:
        channel.start_consuming()
    finally:
        connection.close()

# Function to send messages to a queue based on user input
def send_messages(send_queue, side_name, to_side, prompt):
    connection, channel = create_channel(send_queue)        # Create a channel to send messages to the specified queue

    # Print instructions for the user
    print(f"Side {side_name} started. Type a message and press Enter.")
    print("Type exit or quit to stop.")

    try:
        while True:
            message = input(f"{prompt}> ").strip()
            if message.lower() in EXIT_WORDS:
                break
            if not message:
                continue
            
            # Publish the message to the specified queue
            channel.basic_publish(
                exchange="",                            # Use the default exchange
                routing_key=send_queue,                 # Set the routing key to the send queue
                body=message,                           # Set the message body to the user input  
            )
            print(f"sent to {to_side}: {message}")
    finally:
        connection.close()

# Main function to start the chat application for a given side
def start_chat(side_name, prompt, send_queue, receive_queue, from_side, to_side):
    thread = threading.Thread(
        target=receive_messages,                        # Start the receive_messages function in a separate thread to allow simultaneous sending and receiving
        args=(receive_queue, from_side, prompt),        # Pass the receive queue, sender identifier, and prompt to the receive_messages function
        daemon=True,                                    # Set the thread as a daemon so it will automatically close when the main thread exits
    )
    thread.start()
    # Start sending messages in the main thread
    send_messages(send_queue, side_name, to_side, prompt)
