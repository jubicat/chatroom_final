import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(e)
            break

def main():
    client_socket = socket.socket()
    server_ip = "127.0.0.1"
    server_port = 8888
    client_socket.connect((server_ip, server_port))

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    client_socket.send(f"{username},{password}".encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("enter a message: ")
        if message.startswith('/join'):
            room_name = message.split(' ')[1]
            client_socket.send(message.encode('utf-8'))
            print(f'Joined room: {room_name}')
        elif message.startswith('/create'):
            room_name = message.split(' ')[1]
            client_socket.send(message.encode('utf-8'))
            print(f'Created room: {room_name}')
        elif message.startswith('/delete'):
            room_name = message.split(' ')[1]
            client_socket.send(message.encode('utf-8'))
            print(f'Deleted room: {room_name}')
        elif message.startswith('/leave'):
            room_name = message.split(' ')[1]
            client_socket.send(message.encode('utf-8'))
            print(f'Left room: {room_name}')
        elif message.startswith('/quit'):
            print('Leaving chat room.')
            client_socket.send(message.encode('utf-8'))
            break
        elif message.startswith('/list'):
            print('Available commands:')
            print('/join <room_name>')
            print('/create <room_name>')
            print('/delete <room_name>')
            print('/leave <room_name>')
            print('/quit')
        else:
            send_message = f'{username}: {message}'
            client_socket.send(send_message.encode('utf-8'))

if __name__ == "__main__":
    main()
