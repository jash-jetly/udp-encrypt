import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

server_ip = '127.0.0.1'
server_port = 12346
buffer_size = 1024

# Shared key (must match the server's key)
key = b'4mXrR3rboJOfB9tkGqdmP-Zo7M74-3WhPh7r7cL9bDg='
cipher_suite = Fernet(key)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive_messages():
    while True:
        try:
            encrypted_message, _ = client_socket.recvfrom(buffer_size)
            decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, f"\n{decrypted_message}", 'receiver')
            chat_area.config(state=tk.DISABLED)
            chat_area.see(tk.END)
        except Exception as e:
            print(f"Error: {e}")
            break

def send_message():
    message = message_input.get()
    if message:
        encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
        client_socket.sendto(encrypted_message, (server_ip, server_port))
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"\nYou: {message}", 'sender')
        chat_area.config(state=tk.DISABLED)
        message_input.delete(0, tk.END)
        chat_area.see(tk.END)

root = tk.Tk()
root.title("UDP Chatroom v2 - Encrypted")
root.geometry("400x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
chat_area.tag_config('sender', foreground='blue', justify='right')
chat_area.tag_config('receiver', foreground='green', justify='left')
chat_area.pack(padx=10, pady=10)

message_input = tk.Entry(root, width=40)
message_input.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

root.mainloop()

client_socket.close()

