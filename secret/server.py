import socket
import threading
import sys
from cryptography.fernet import Fernet
from typing import Union

SECRET_KEY = b"jxg8NHEAdwOgcvd968-pXfu-qG16nWBaqppRXUqfiUM="

is_keyboard_interrupted = False


def decrypt_packet(packet):
    f_ = Fernet(SECRET_KEY)
    data = f_.decrypt(packet)
    return data.decode()


def handle_client(conn: socket.socket):
    while True:
        data = conn.recv(1024)
        if not data:
            print("not data")
            break

        print(f"encrypted - {data}")
        data = decrypt_packet(data)
        print(f"decrypted - {data}", end="\n")
        print(f"{'------'*10}")

        if data.strip() == "exit":
            exit()
        if is_keyboard_interrupted:
            exit()
        # sleep(5)


def main():
    global is_keyboard_interrupted
    while True:
        try:
            with socket.create_server(
                address=("localhost", 5678), family=socket.AF_INET
            ) as server:
                while True:
                    conn, addr = server.accept()
                    print(f"connected by {addr}")
                    client_thread = threading.Thread(target=handle_client, args=(conn,))
                    client_thread.start()

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            is_keyboard_interrupted = True
            sys.exit("Keyboard Interrupted")


if __name__ == "__main__":
    main()
