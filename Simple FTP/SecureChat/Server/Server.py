# server.py

import socket
import threading
import json
import bcrypt  # For secure password hashing

clients = {}  # Store connected clients by username

# Load credentials
def load_credentials():
    with open("C:/Users/Blanc/Desktop/Server/credentials.json", "r") as file:
        return json.load(file)

# Authenticate user
def authenticate(username, password):
    credentials = load_credentials()
    print(f"Authenticating user: {username} with password: {password}")
    
    if username in credentials:
        stored_hash = credentials[username]
        print(f"Stored hash for {username}: {stored_hash}")  # Debugging line

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):  # Ensure both are bytes
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed: Incorrect password")
            return False
    print(f"Authentication failed: {username} not found")
    return False


# Handle client connections
def handle_client(client_socket):
    try:
        # Receive authentication data
        auth_data = client_socket.recv(1024).decode('utf-8')
        username, password = auth_data.split(',')
        
        if authenticate(username, password):
            client_socket.send("AUTH_SUCCESS".encode('utf-8'))
            print(f"User {username} authenticated")
            clients[username] = client_socket
            relay_messages(client_socket, username)
        else:
            client_socket.send("AUTH_FAIL".encode('utf-8'))
            client_socket.close()
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.close()

# Relay messages between clients
def relay_messages(client_socket, username):
    try:
        while True:
            # Receive encrypted message
            data = client_socket.recv(4096)
            if not data:
                break

            # Decode recipient and encrypted message
            recipient, encrypted_message = data.decode('utf-8').split("||", 1)

            print(f"Received encrypted message for {recipient}: {encrypted_message}")

            # Forward the encrypted message to the recipient if they are online
            if recipient in clients:
                # Forward only sender information and encrypted message
                clients[recipient].send(f"{username}||{encrypted_message}".encode('utf-8'))
            else:
                client_socket.send("Recipient not online".encode('utf-8'))

    except Exception as e:
        print(f"Error relaying messages: {e}")
    finally:
        print(f"User {username} disconnected")
        del clients[username]
        client_socket.close()

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("Server is running...")
    while True:
        client_socket, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Run server
if __name__ == "__main__":
    start_server()
z
