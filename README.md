# udp-encryption-server
The README for the UDP Encryption Server project is a comprehensive guide to a Python-based client-server application designed for CSC 442 Network Programming. It combines UDP sockets with AES-256 encryption to handle text encryption and decryption

across multiple clients.

Project Overview

This project implements a secure UDP-based server that encrypts and decrypts messages using AES-256 in CBC mode. It's ideal for exploring network programming and cryptography, allowing clients to send plain text for encryption or base64-encoded 

ciphertexts for decryption. The server acts like a "cryptographic bouncer," managing secrets with efficiency and a touch of whimsy, supporting multiple concurrent connections via threading.

Features

AES-256 encryption/decryption with PKCS7 padding and base64 encoding for safe transmission.

Multi-client handling through Python's _thread module for simultaneous operations.

UDP communication for lightweight, connectionless exchanges.

Simple command interface: ENCRYPT:<text>, DECRYPT:<base64>, and TERMINATE, with built-in error responses.

Random key generation on startup, ensuring session-specific security.

Prerequisites

Python 3.6+.

The cryptography library (install via pip install cryptography).

Git for cloning the repository.

A terminal (e.g., PowerShell or Git Bash) and a non-cloud-synced folder to avoid issues like OneDrive interference.

Installation

Clone the repo: git clone https://github.com/Ehxzel/udp-encryption-server.git and navigate into the directory.

Install dependencies: pip install cryptography.

Relocate to a safe folder (e.g., C:\Projects) to prevent sync-related Git corruptions.

Usage

Server: Run python server.py to start on 127.0.0.1:8006. It generates a key and listens for clients.

Client: In another terminal, run python client.py. Input commands like ENCRYPT:Hello, World! (gets encrypted response), DECRYPT:<ciphertext> (decrypted if valid), or TERMINATE (closes connection).

Stop server with Ctrl+C.

Example: Encrypt a message, decrypt the result, then terminate—responses are displayed clearly.

How It Works

Server (server.py): Binds a UDP socket, generates a 32-byte AES key, and spawns threads per client. Processes commands in a loop using the AESCipher class for encryption (with random IV) and decryption, sending ASCII responses.

Client (client.py): Sends user-input commands via UDP and prints server replies, closing on TERMINATE or error.

AESCipher: Custom class handling AES operations, including padding and base64 for transmission safety.

Threading ensures smooth multi-client support, like a host managing a lively party.

File Structure

server.py: Core server logic with encryption.

client.py: Client-side command sender.

README.md: Project documentation.

LICENSE: Legal terms.

.gitignore: Excludes unnecessary files (e.g., Python bytecode).

Security Notes

Keys are random and non-persistent; for real-world use, implement secure storage.

UDP's connectionless nature means potential packet loss—best for local testing.

Limited to localhost (127.0.0.1) to minimize exposure.

Errors (e.g., invalid ciphertext) are handled with informative messages.

Troubleshooting

Missing library: Reinstall cryptography.

Connection issues: Confirm server is running and ports match.

Decryption errors: Ensure ciphertext matches the session's key.

Git problems (e.g., config corruption): Move out of synced folders like OneDrive and reinitialize.

Editor hangs: Set Git editor to Notepad or VS Code via git config --global core.editor "notepad".

Contributing

Fork the repo, make changes, and submit pull requests. Discuss major ideas via issues first—witty commit messages encouraged.

License

Covered in the LICENSE file (likely MIT or similar—check for details).

Acknowledgements

Thanks to CSC 442, the cryptography library, and the internet for enabling this blend of security and fun. The server's "Ready to play?" prompt invites users to engage playfully.
