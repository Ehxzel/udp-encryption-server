import socket
from _thread import *
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# AES Encryption Class
class AESCipher:
    def __init__(self, key: bytes):
        self.key = key
        self.backend = default_backend()
        self.block_size = algorithms.AES.block_size

    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + ct).decode()

    def decrypt(self, b64_ciphertext: str) -> str:
        try:
            data = base64.b64decode(b64_ciphertext)
            print(data) 
            iv = data[:16]
            ct = data[16:]
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ct) + decryptor.finalize()
            unpadder = padding.PKCS7(self.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            return plaintext.decode()
        except Exception as e:
            return f"DECRYPTION ERROR: {str(e)}"

print("Ready to play?")
# Server setup
th = 0
ss = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("Server Start:")

host = '127.0.0.1'
port = 8006
ss.bind((host, port))

key = os.urandom(32)  # AES-256 key
cipher = AESCipher(key)
clients = set()  # Track client addresses

def client_thread(client_addr):
    global th
    while True:
        try:
            data, addr = ss.recvfrom(1024)
            if addr != client_addr:  # Ignore messages from other clients
                continue
            if not data:
                break
            print(f'Thread {th} message without decoding: {data}')
            message = data.decode().strip()
            print(f'Thread {th} message with decoding: {message}')

            if message.startswith("ENCRYPT:"):
                plaintext = message[8:].strip()
                encrypted = cipher.encrypt(plaintext)
                ss.sendto(f"ENCRYPTED:{encrypted}\n".encode("ascii"), client_addr)
            elif message.startswith("DECRYPT:"):
                encrypted_text = message[8:].strip()
                decrypted = cipher.decrypt(encrypted_text)
                if decrypted.startswith("DECRYPTION ERROR"):
                    ss.sendto(f"ERROR:{decrypted}\n".encode("ascii"), client_addr)
                else:
                    ss.sendto(f"DECRYPTED:{decrypted}\n".encode("ascii"), client_addr)
            elif message == "TERMINATE":
                ss.sendto(b"BYE\n", client_addr)
                break
            else:
                ss.sendto(b"ERROR:Unknown command\n", client_addr)
        except Exception as e:
            ss.sendto(f"ERROR: {str(e)}\n".encode("ascii"), client_addr)
            break
    print(f'Thread {th}: Client {client_addr} disconnected')

while True:
    try:
        data, addr = ss.recvfrom(1024)
        if addr not in clients:
            clients.add(addr)
            print(f'address client: {addr[0]}\nport number: {addr[1]}')
            th += 1
            start_new_thread(client_thread, (addr,))
            print(f'\nthread no: {th}\nprocess id: {os.getpid()}\n')
            # Process the first message
            message = data.decode().strip()
            print(f'Thread {th} message with decoding: {message}')
            if message.startswith("ENCRYPT:"):
                plaintext = message[8:].strip()
                encrypted = cipher.encrypt(plaintext)
                ss.sendto(f"ENCRYPTED:{encrypted}\n".encode("ascii"), addr)
            elif message.startswith("DECRYPT:"):
                encrypted_text = message[8:].strip()
                decrypted = cipher.decrypt(encrypted_text)
                if decrypted.startswith("DECRYPTION ERROR"):
                    ss.sendto(f"ERROR:{decrypted}\n".encode("ascii"), addr)
                else:
                    ss.sendto(f"DECRYPTED:{decrypted}\n".encode("ascii"), addr)
            elif message == "TERMINATE":
                ss.sendto(b"BYE\n", addr)
            else:
                ss.sendto(b"ERROR:Unknown command\n", addr)
    except KeyboardInterrupt:
        print("Server shutting down...")
        break

ss.close()
