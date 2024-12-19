import socket
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import scrolledtext
import threading  # For receiving messages in a separate thread

# Load the encryption key
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Encrypt a message
def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode('utf-8'))

# Decrypt a message
def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode('utf-8')

# Connect to the server and authenticate
def connect_to_server(username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))

    # Send authentication data (username and password)
    auth_data = f"{username},{password}"
    client.send(auth_data.encode('utf-8'))

    # Receive authentication response
    response = client.recv(1024).decode('utf-8')
    if response == "AUTH_SUCCESS":
        print(f"{username} authenticated successfully!")
        return client
    else:
        print(f"{username} authentication failed!")
        client.close()
        return None

# Send encrypted message to the server
def send_message(client, message, recipient, key, username):
    # Encrypt the message
    encrypted_message = encrypt_message(message, key)
    
    # Format the data for the server (include recipient only for routing purposes)
    data = f"{recipient}||from {username}||{encrypted_message.decode('utf-8')}"
    
    print(f"Sending to server: {data}")  # Debug for what is sent
    client.send(data.encode('utf-8'))

# Function to receive messages from the server
def receive_message(client, key, chat_box):
    while True:
        try:
            # Receive message from the server
            data = client.recv(4096).decode('utf-8')
            if data:
                # Debug: Print the received raw message
                print(f"Received from server: {data}")

                # Parse the message (sender||<encrypted_message>)
                parts = data.split("||", 2)  # Split into at most 3 parts
                if len(parts) == 3:
                    sender = parts[0]  # First part is the sender
                    encrypted_message = parts[2]  # Third part is the encrypted message
                    
                    # Decrypt the message
                    decrypted_message = decrypt_message(encrypted_message.encode('utf-8'), key)
                    print(f"Decrypted message from {sender}: {decrypted_message}")

                    # Display the message in the chat box with the sender's name
                    chat_box.insert(tk.END, f"{sender}: {decrypted_message}\n")
                else:
                    print("Error: Received message in incorrect format.")
            else:
                print("No data received or connection lost.")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


# Create the chat GUI
def chat_ui(client, key):
    def send_message_gui():
        message = message_input.get()
        recipient = recipient_input.get()
        if message and recipient:
            if recipient == username:
                chat_box.insert(tk.END, "Error: You cannot message yourself.\n")
                message_input.delete(0, tk.END)
                return
            send_message(client, message, recipient, key, username)
            chat_box.insert(tk.END, f"You: {message}\n")
            message_input.delete(0, tk.END)

    root = tk.Tk()
    root.title(username)

    chat_box = scrolledtext.ScrolledText(root, width=50, height=20)
    chat_box.pack(padx=10, pady=10)

    recipient_input = tk.Entry(root, width=40)
    recipient_input.pack(side=tk.LEFT, padx=10, pady=10)
    recipient_input.insert(0, "kitty")

    message_input = tk.Entry(root, width=40)
    message_input.pack(side=tk.LEFT, padx=10, pady=10)
    message_input.insert(0, "Woof Woof")

    send_button = tk.Button(root, text="Send", command=send_message_gui)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Start a thread to receive messages
    threading.Thread(target=receive_message, args=(client, key, chat_box), daemon=True).start()

    root.mainloop()
# Example usage
if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")

    # Connect to the server and authenticate
    client = connect_to_server(username, password)
    if client:
        # Load encryption key
        key = load_key()

        # Run chat UI
        chat_ui(client, key)
