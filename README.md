# Readme for RSA Encryption and Chat Server/Client

This repository contains Python code for two distinct functionalities:

1. RSA Encryption (`rsa.py`):
   - RSA encryption and decryption code that allows you to securely encrypt and decrypt messages using RSA cryptography.
   - You can generate key pairs, encrypt messages, and decrypt messages using the RSA algorithm.
   - The code includes functions for generating key pairs, encrypting, and decrypting messages.

2. Chat Server and Client (`server.py` and `client.py`):
   - A basic chat server and client implementation where users can connect, create chat rooms, send and receive messages within chat rooms.
   - The server handles user registration, message routing, and room management.
   - The client allows users to connect, send and receive messages, create rooms, and perform various chat-related operations.

## RSA Encryption (`rsa.py`)

### Usage

To use the RSA encryption code:

1. Import the `rsa` module.
2. Generate RSA key pairs using `generate_key_pair(p, q)` where `p` and `q` are prime numbers.
3. Encrypt a message using `encrypt(pk, plaintext)` with the public key.
4. Decrypt a ciphertext using `decrypt(pk, ciphertext)` with the private key.

Example usage:
```python
import rsa

# Generate key pairs
public_key, private_key = rsa.generate_key_pair(p, q)

# Encrypt and decrypt a message
message = "Hello, World!"
encrypted = rsa.encrypt(public_key, message)
decrypted = rsa.decrypt(private_key, encrypted)

print("Original message:", message)
print("Encrypted message:", encrypted)
print("Decrypted message:", decrypted)
```

## Chat Server and Client (`server.py` and `client.py`)

### Server (`server.py`)

The server creates a chat room environment where users can connect, create rooms, send and receive messages. It also handles user registration and disconnection.

### Client (`client.py`)

The client connects to the server and allows users to interact with the chat server. Users can send messages, create rooms, and perform various chat-related operations.

### Usage

1. Run the server (`server.py`) on a machine, specifying the IP address and port.
2. Run one or more clients (`client.py`) on different machines, specifying the server's IP address and port.
3. Clients can register with a username and password.
4. Clients can send messages, create rooms, join rooms, leave rooms, and perform other chat-related actions.

Example usage:

- Run the server:
  ```bash
  python server.py
  ```

- Run multiple clients (on different machines):

  ```bash
  python client.py
  ```

- Enter a username and password for each client when prompted.

- Use commands such as `/join`, `/leave`, `/create`, `/delete`, and `/quit` to interact with the chat server.

- Type regular messages to chat with other users in the same room.

Please note that this is a basic chat server and client implementation and can be extended or modified for more complex chat applications.

## Dependencies

The code for both RSA encryption and the chat server/client uses only Python's built-in libraries and doesn't require additional dependencies.

Feel free to explore, modify, and build upon this code for your specific needs.