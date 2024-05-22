# import os
# import base64
import socket
from cryptography.fernet import Fernet

host = "localhost"
port = 5678
# Generate a random key (replace with your own secure key generation method)
# key = os.urandom(32)

# # Encode the key to URL-safe base64
# encoded_key = base64.urlsafe_b64encode(key).decode()

# # Assign the encoded key to the secret variable
# secret = encoded_key.encode()
# print(secret)
secret = b'jxg8NHEAdwOgcvd968-pXfu-qG16nWBaqppRXUqfiUM='

def encrypt_packet(packet):
    f_ = Fernet(secret)
    data = f_.encrypt(packet)
    return data


def main():
    with socket.create_connection((host, port)) as client:
        while True:
            data = input("Client: ").strip().encode()
            encrypted_data = encrypt_packet(data)
            print(encrypted_data)
            client.sendall(encrypted_data)
            if data == "exit":
                break

if __name__ == "__main__":
    main()
