import socket
from app_utils.crypto import Crypto
from app_utils.http import ClientHttp
from app_utils.config import client_config


class Client:
    def __init__(self):
        self.client_config = client_config()
        self.http = ClientHttp()
        self.client_info = self.http.get_client_info()
        self.load_keys()
        self.crypto = Crypto(self.server_public_key, self.client_private_key)

    def load_keys(self):
        self.client_private_key = self.http.get_client_private_key()
        self.server_public_key = self.http.get_server_public_key()

    def messaging(self):
        with socket.create_connection(
            (self.client_config.target_host, self.client_config.target_port)
        ) as conn:
            while True:
                data = input("client: ").strip()
                encrypted_data = self.crypto.encrypt(data)
                print(encrypted_data)
                conn.sendall(encrypted_data.encode())
                if data == "exit":
                    break
