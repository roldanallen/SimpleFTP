from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# File paths for client and server
client_key_path = r"C:\Users\Blanc\Desktop\Client\key.key"
server_key_path = r"C:\Users\Blanc\Desktop\Server\key.key"

# Write the key to both file locations
with open(client_key_path, "wb") as client_key_file:
    client_key_file.write(key)

with open(server_key_path, "wb") as server_key_file:
    server_key_file.write(key)
