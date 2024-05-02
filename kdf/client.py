# Client side
from cryptography.hazmat.primitives.asymmetric import dh, padding
from cryptography.hazmat.primitives import serialization

# Generate client's private and public key for Diffie-Hellman key exchange
parameters = dh.generate_parameters(generator=2, key_size=2048)
client_private_key = parameters.generate_private_key()
client_public_key = client_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

client_private_key_bytes = client_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),  # No encryption
)
print(client_private_key_bytes)
print(client_public_key)

client_private_key = b'-----BEGIN PRIVATE KEY-----\nMIICJgIBADCCARcGCSqGSIb3DQEDATCCAQgCggEBAIptG0s/JqCCbsmuwJJqqx7/\npUE6UYBaHP79U4LgRD1WLrAkp3gv15ik5bPxi3+cBNlOjmBra8saFhzjMz9kym1R\njGoWQ9nE2rF0fsjL0l8T67uEh+zvb4DgWEEQ7aaTgxxeLVPeggvRXiRrFerpS/vi\nFqSKEoDbLlCPrxrKFeO8OpArhcvAobkcQaTayfDOwe9FRnqq8x4K1WVIGXlpe7Hm\nyJOro9E8K6JaweYrx/j7n952cVSeQ24UMhB+0M55VFyAbaQ4hTjFHiPNfYrIdD0k\nlrpBIbDEXKsB0E8/z4D0BhoTVR7h/Dn8cR/iAa4Uok69OScSaJSDGQNQS4cjiscC\nAQIEggEEAoIBAERQfDtTPQZhU51wcfIhJIAJMBDm5thfxliZiTH8myUoQxi64Tp3\nEJire/Bfzh5tFhnkLb/auITq2RFbQw4oXjuJYLdokunyVBgMGeaczRQyNx6xneNT\nQqDZyb9IprwXP9PmS6S9uTxZTj+tSqlS7zX8yvnNQqLI2YyrHRNgo56nAgQr9J5M\npF4gGgZX6A9GvdYgrL7eDTg3KVPnSZxg7agaQNhv77ZDFyItBZPI+hJi+D2yZH9+\n4kyMnrr34owdmDVzsfPLvmhn/17m+sid6dRryF31IcgIr3uWZVzdoMfUcNlI02do\nRtwkZ+Ip1y/Mfnv0lpopVIkmIOJ7SHy/vfo=\n-----END PRIVATE KEY-----\n'

client_public_key = b'-----BEGIN PUBLIC KEY-----\nMIICJDCCARcGCSqGSIb3DQEDATCCAQgCggEBAIptG0s/JqCCbsmuwJJqqx7/pUE6\nUYBaHP79U4LgRD1WLrAkp3gv15ik5bPxi3+cBNlOjmBra8saFhzjMz9kym1RjGoW\nQ9nE2rF0fsjL0l8T67uEh+zvb4DgWEEQ7aaTgxxeLVPeggvRXiRrFerpS/viFqSK\nEoDbLlCPrxrKFeO8OpArhcvAobkcQaTayfDOwe9FRnqq8x4K1WVIGXlpe7HmyJOr\no9E8K6JaweYrx/j7n952cVSeQ24UMhB+0M55VFyAbaQ4hTjFHiPNfYrIdD0klrpB\nIbDEXKsB0E8/z4D0BhoTVR7h/Dn8cR/iAa4Uok69OScSaJSDGQNQS4cjiscCAQID\nggEFAAKCAQA+xbmJGYzp5HO00Pgduoy8cfrRY2c8ablCVimX3qb/LJvmXfF2fkfU\n1SaBY4iUHLD1cZdEu0qpGRDiT8mHd0HyXzEozPFlrtJ2rfrUC+fxW+VwRQP32DFa\nfEojPyXG+tF7vkEA4uJvv9Wr8p0MSEbDUbJyjhTD0BEiZS94DqIAyDVQS0iFgzuB\nyf0PU2Z6RHUrzhoaJXOudEbtEVbW0H1AOxWC2DiQOFwHBOn2KQIiA7snO/lD0F9F\nM9P2FnALagVxlk17X6b/XfhcgUaG5aU2SfUtxC0Zx9gfEfbbmF7Gh8yy5rfZH6y+\nfW0kIy12aSxxouVQYgjgTqmomP7iYOGk\n-----END PUBLIC KEY-----\n'
# Send client's public key to the server
# send_data_to_server(client_public_key)

# Receive server's public key from the server
# server_public_key = receive_data_from_server()

# Derive shared secret using client's private key and server's public key
# shared_key = client_private_key.exchange(server_public_key)

# Use shared_key for symmetric encryption
