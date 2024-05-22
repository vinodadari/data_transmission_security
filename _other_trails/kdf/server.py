# Server side
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

# Generate server's private and public key for Diffie-Hellman key exchange
parameters = dh.generate_parameters(generator=2, key_size=2048)
server_private_key = parameters.generate_private_key()
server_public_key = server_private_key.public_key().public_bytes(
    encoding=Encoding.PEM,
    format=PublicFormat.SubjectPublicKeyInfo,
)

# Send server's public key to the client
# send_data_to_client(server_public_key)

# Receive client's public key from the client
# client_public_key = receive_data_from_client()

# Load client's public key
client_public_key = b'-----BEGIN PUBLIC KEY-----\nMIICJDCCARcGCSqGSIb3DQEDATCCAQgCggEBAIptG0s/JqCCbsmuwJJqqx7/pUE6\nUYBaHP79U4LgRD1WLrAkp3gv15ik5bPxi3+cBNlOjmBra8saFhzjMz9kym1RjGoW\nQ9nE2rF0fsjL0l8T67uEh+zvb4DgWEEQ7aaTgxxeLVPeggvRXiRrFerpS/viFqSK\nEoDbLlCPrxrKFeO8OpArhcvAobkcQaTayfDOwe9FRnqq8x4K1WVIGXlpe7HmyJOr\no9E8K6JaweYrx/j7n952cVSeQ24UMhB+0M55VFyAbaQ4hTjFHiPNfYrIdD0klrpB\nIbDEXKsB0E8/z4D0BhoTVR7h/Dn8cR/iAa4Uok69OScSaJSDGQNQS4cjiscCAQID\nggEFAAKCAQA+xbmJGYzp5HO00Pgduoy8cfrRY2c8ablCVimX3qb/LJvmXfF2fkfU\n1SaBY4iUHLD1cZdEu0qpGRDiT8mHd0HyXzEozPFlrtJ2rfrUC+fxW+VwRQP32DFa\nfEojPyXG+tF7vkEA4uJvv9Wr8p0MSEbDUbJyjhTD0BEiZS94DqIAyDVQS0iFgzuB\nyf0PU2Z6RHUrzhoaJXOudEbtEVbW0H1AOxWC2DiQOFwHBOn2KQIiA7snO/lD0F9F\nM9P2FnALagVxlk17X6b/XfhcgUaG5aU2SfUtxC0Zx9gfEfbbmF7Gh8yy5rfZH6y+\nfW0kIy12aSxxouVQYgjgTqmomP7iYOGk\n-----END PUBLIC KEY-----\n'
client_public_key_obj = serialization.load_pem_public_key(
    client_public_key,
    backend=default_backend()
)

# Derive shared secret using server's private key and client's public key
shared_key = server_private_key.exchange(client_public_key_obj)

print("Shared key:", shared_key)

# Use shared_key for symmetric encryption
# For example, you can use it with AES
