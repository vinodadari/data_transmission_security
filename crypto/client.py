# pip install pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate or load client's public and private keys
client_private_key = RSA.generate(2048)
client_public_key = client_private_key.publickey()
print(client_private_key)
print(client_public_key.export_key())

# Generate or load server's public and private keys
server_private_key = RSA.generate(2048)
server_public_key = server_private_key.publickey()

# Simulating client sending a message to server
message_to_server = b"Hello Server!"

# Encrypt the message using server's public key
cipher = PKCS1_OAEP.new(server_public_key)
encrypted_message_to_server = cipher.encrypt(message_to_server)
print(encrypted_message_to_server)
# Simulating server receiving and decrypting the message
cipher = PKCS1_OAEP.new(server_private_key)
decrypted_message_from_client = cipher.decrypt(encrypted_message_to_server)

print("Server received message from client:", decrypted_message_from_client.decode())

# Simulating server sending a message to client
message_to_client = b"Hello Client!"

# Encrypt the message using client's public key
cipher = PKCS1_OAEP.new(client_public_key)
encrypted_message_to_client = cipher.encrypt(message_to_client)
print(encrypted_message_to_client)

# Simulating client receiving and decrypting the message
cipher = PKCS1_OAEP.new(client_private_key)
decrypted_message_from_server = cipher.decrypt(encrypted_message_to_client)

print("Client received message from server:", decrypted_message_from_server.decode())
