from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64


class Crypto:
    def __init__(self, pubic_key: str, private_key: str):
        self.public_key = pubic_key
        self.private_key = private_key

    def encrypt(self, data: str) -> str:
        public_key = RSA.import_key(self.public_key)
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_data = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()

    def decrypt(self, data: str) -> str:
        private_key = RSA.import_key(self.private_key)
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(base64.b64decode(data)).decode()
        return decrypted_data
