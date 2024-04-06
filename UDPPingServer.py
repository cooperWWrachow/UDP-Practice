#############################
# Name: Cooper Rachow       #
# Date: 2/5/24              #
# Assignment: Ping over UDP #
#############################

from socket import *
from random import randint

# Set the server IP address and port number
server_ip = "192.168.1.165"  # Listen on all available network interfaces i.e. 192.168.1.165
server_port = 12000  # Choose a port number (e.g., 12345)

# Create a UDP socket for the server
server_socket = socket(AF_INET, SOCK_DGRAM)

# Bind the server socket to a specific IP address ('' means all available interfaces) and port 12000
server_socket.bind((server_ip, server_port))

# Enter an infinite loop to keep the server running
while True:

    # Receive a message and the client's address from the client socket
    message, client_address = server_socket.recvfrom(2048)

    message = message.decode()
    
    # random loss generator 
    if randint(1, 10) <= 4:
        continue

    # send message back if it passes the loss generator 
    server_socket.sendto(message.encode(), client_address)



