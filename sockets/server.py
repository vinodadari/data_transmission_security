import socket
from app_utils.crypto import Crypto
from app_utils.http import ServerHttp
from app_utils.config import server_config


class Client:
    def __init__(self):
        self.server_config = server_config()
        self.http = ServerHttp()
        self.client_info = self.http.get_server_info()
        self.load_keys()
        self.crypto = Crypto(self.server_private_key, self.client_public_key)

    def load_keys(self):
        self.client_public_key = self.http.get_client_public_key()
        self.server_private_key = self.http.get_server_private_key()

    def messaging(self):
        with socket.create_server(
            (self.server_config.bind_host, self.server_config.bind_port)
        ) as server:
            while True:
                conn, addr = server.accept()
                data = conn.recv(1024).decode()
                if not data:
                    break
                decrypt_msg = self.crypto.decrypt(data)
                print(decrypt_msg)

                if decrypt_msg.strip() == "exit":
                    break
