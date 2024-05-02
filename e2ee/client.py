import socket
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding

# Replace with a strong password (same as server)
CLIENT_PASSWORD = b"vinod"


def generate_key_pair():
    """
    Generates a key pair (private and public key).

    Returns:
        A tuple containing the private key (PEM format) and public key (byte string).
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key().public_bytes(
        encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_key


def derive_key(server_public_key, client_private_key):
    """
    Derives a key from the server's public key and client's private key.

    Args:
        server_public_key: The server's public key (PEM format).
        client_private_key: The client's private key object.

    Returns:
        A Fernet key derived from the combination.
    """
    client_public_key = client_private_key.public_key().public_bytes(
        encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
    )
    key_exchange = client_private_key.decrypt(
        server_public_key,
        padding.OAEP(  # Fix the attribute name here
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
    )
    shared_secret = key_exchange + client_public_key

    print(f"server public key - {server_public_key}", end="\n\n")
    print(f"client private key - {client_private_key}", end="\n\n")
    print(f"client public key - {client_public_key}", end="\n\n")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=shared_secret, iterations=390000
    )
    derived_key = kdf.derive(CLIENT_PASSWORD)

    # Encode the derived key as base64
    fernet_key = base64.urlsafe_b64encode(derived_key)

    return fernet_key


def send_message(conn, message, fernet):
    """
    Sends an encrypted message to the server.

    Args:
        conn: The socket object for the client connection.
        message: The message to send (string).
        fernet: The Fernet object for encryption.
    """
    encrypted_data = fernet.encrypt(message.encode())
    conn.sendall(encrypted_data)


def main():
    HOST = "localhost"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    client_private_key, client_public_key = generate_key_pair()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Send client's public key to the server
        s.sendall(client_public_key)
        print("client public key has been sent")

        # Receive server's public key (assuming sent after connection)
        server_public_key = s.recv(1024)
        print(f"received server's public key - {server_public_key}")

        # Derive encryption key based on exchanged keys and password
        key = derive_key(server_public_key, client_private_key)
        fernet = Fernet(key)
        print(f"token - {key}")

        while True:
            message = input("Enter message: ")
            if message == "quit":
                break
            send_message(s, message, fernet)

            # Simulate receiving a response (already decrypted by server)
            data = s.recv(1024)
            print(f"Received response: {data.decode()}")

    print("Connection closed.")


if __name__ == "__main__":
    main()
