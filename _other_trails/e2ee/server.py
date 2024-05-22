import base64
import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2PasswordHasher
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding

# Replace with a strong password for key derivation
SERVER_PASSWORD = b"vinod"


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


def derive_key(client_public_key, server_private_key):
    """
    Derives a key from the client's public key and server's private key (using PBKDF2HMAC).

    **Note:** This approach is considered less secure than using PBKDF2PasswordHasher.

    Args:
        client_public_key: The client's public key (byte string).
        server_private_key: The server's private key object.

    Returns:
        A Fernet key derived from the combination.
    """
    server_public_key = server_private_key.public_key().public_bytes(
        encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
    )
    key_exchange = server_private_key.decrypt(
        server_public_key,
        padding.OAEP(  # Fix the attribute name here
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
    )
    shared_secret = key_exchange + server_public_key

    print(f"server public key - {server_public_key}", end="\n\n")
    print(f"server private key - {server_private_key}", end="\n\n")
    print(f"client public key - {client_public_key}", end="\n\n")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=shared_secret, iterations=390000
    )
    derived_key =  kdf.derive(SERVER_PASSWORD)
    fernet_key = base64.urlsafe_b64encode(derived_key)

    return fernet_key


def handle_client(conn, client_public_key):
    """
    Handles communication with a connected client.

    Args:
        conn: The socket object for the client connection.
        client_public_key: The client's public key (byte string).
    """
    server_private_key, _ = (
        generate_key_pair()
    )  # Generate server key pair if not done already
    key = derive_key(client_public_key, server_private_key)
    fernet = Fernet(key)
    print(f"token - {key}")
    conn.sendall(_)
    while True:
        data = conn.recv(1024)
        if not data:
            break

        # Decrypt received message
        decrypted_data = fernet.decrypt(data).decode()
        print(f"Received encrypted message: {data}")
        print(f"Decrypted message from client: {decrypted_data}")

        # Simulate processing and sending a response (unencrypted)
        response = "Message received!"
        conn.sendall(fernet.encrypt(response.encode()))  # Encrypt response
    conn.close()


def main():
    HOST = "localhost"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            # Receive client's public key (assuming sent during initial connection)
            client_public_key = conn.recv(1024)
            print(f"received client public key - {client_public_key}")

            handle_client(conn, client_public_key)


if __name__ == "__main__":
    main()
