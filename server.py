import socket
import threading
from cryptography.fernet import Fernet

server_ip = '127.0.0.1'
server_port = 12346
buffer_size = 1024
clients = []

# Shared key (generate a key once and use the same here)
key = b'4mXrR3rboJOfB9tkGqdmP-Zo7M74-3WhPh7r7cL9bDg='
cipher_suite = Fernet(key)

def broadcast(message, sender_address):
    for client in clients:
        if client != sender_address:
            server_socket.sendto(message, client)

def handle_client():
    while True:
        encrypted_message, client_address = server_socket.recvfrom(buffer_size)
        if client_address not in clients:
            clients.append(client_address)
        broadcast(encrypted_message, client_address)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

thread = threading.Thread(target=handle_client)
thread.daemon = True
thread.start()

print("Server is running...")

while True:
    pass
while True:
    pass

