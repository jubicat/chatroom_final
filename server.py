import os
import socket
import threading

class ChatRoomApp:
    def __init__(self, server_ip, server_port, server_socket, names, rooms, clients):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = server_socket
        self.names = names
        self.rooms = rooms
        self.clients = clients

    def add_user(self, user, client_socket):
        """
        Create a new user in the server
        Add username, password, and IP address to the server
        """

        if user[0] in names:
            if user[1] == names[user[0]]["password"]:
                names[user[0]]["ip"] = user[2]
                clients.append(client_socket)
                print("User reconnected: {}".format(user[0]))
                print("Users: {}".format(names))
            else:
                print("Incorrect password")
                client_socket.send("Incorrect password".encode('utf-8'))
        
        username, password, ip = user
        names[username] = {
            "password": password,
            "ip": ip,
            "rooms": [],
            "current_room": ""
        }

        clients.append(client_socket)
        print("New user added: {}".format(username))
        print("Users: {}".format(names))

    def remove_user(self, username):
        """
        Delete a user from the server
        """
        if username in names:
            del names[username]

    def create_room(self, room_name):
        """
        Create a new chatroom in the server
        Store the client addresses and their current rooms
        """
        if room_name in self.rooms:
            print("Room already exists")
            return
        
        rooms[room_name] = {
            "users": []
        }

        print("New room created: {}".format(room_name))
        print("Rooms: {}".format(rooms))

    def delete_room(self, room_name):
        """
        Delete a chatroom and close all connections to it in the server
        """
        if room_name not in rooms:
            print("Room does not exist")
            return
        
        if room_name in rooms:
            for username in rooms[room_name]["users"]:
                self.leave_room(username, room_name)
            del rooms[room_name]

    def get_room(self, room_name):
        """
        Get the room object from the server
        """
        return rooms.get(room_name)

    def close_room_connection(self, room_name):
        """
        Close all connections to a room
        """
        if room_name in rooms:
            for username in rooms[room_name]["users"]:
                for client in clients:
                    username_info = names.get(username)
                    if username_info and username_info["ip"] == client.getpeername():
                        client.close()
                        clients.remove(client)
                        break

    def join_room(self, username, room_name):
        """
        Join a room
        """
        if room_name in rooms and username in names:
            rooms[room_name]["users"].append(username)
            names[username]["rooms"].append(room_name)
            names[username]["current_room"] = room_name

        print("User {} joined room {}".format(username, room_name))
        print("Rooms: {}".format(rooms))

    def leave_room(self, username, room_name):
        """
        User leaves a room and is asked for a new room
        """
        if room_name in rooms and username in names:
            rooms[room_name]["users"].remove(username)
            names[username]["rooms"].remove(room_name)
            if(len(names[username]["rooms"]) > 0):
                names[username]["current_room"] = names[username]["rooms"][0]
            else: names[username]["current_room"] = ""

    def send_message(self, username, message):
        """
        Send a message to all users in the room
        """
        room_name = names[username]["current_room"]
        if room_name in rooms:
            for user in rooms[room_name]["users"]:
                if(user == username):
                    continue
                print("Sending message to {}".format(user))
                print("Usernames: {}".format(names))
                if user in names.keys() and room_name in names[username]["rooms"]:
                    client_index = names[user]["ip"]
                    print("Message: {}".format(message))
                    for client in clients:
                        if client.getpeername() == client_index:
                            client.send(message.encode('utf-8'))

    def close_all(self):
        """
        Close all connections
        """
        for client in clients:
            client.close()

    def main(self):
        print("server is starting...")
        server_socket.bind((self.server_ip, self.server_port))
        server_socket.listen(10)
        print("server is waiting for connection...")
        while True:
            client_socket, client_address = server_socket.accept()
            print("Connected to {} on port {}".format(self.server_ip, self.server_port))
            user_data = client_socket.recv(1024).decode('utf-8')
            if user_data:
                user_data = user_data.split(',')
                username = user_data[0]
                password = user_data[1]
                user_ip = client_address
                self.add_user((username, password, user_ip), client_socket)
                t = threading.Thread(target=self.handle_client, args=(client_socket, username))
                t.start()

    def handle_client(self, client_socket, username):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message.startswith('/create'):
                    room_name = message.split(' ')[1]
                    self.create_room(room_name)
                elif message.startswith('/delete'):
                    room_name = message.split(' ')[1]
                    self.delete_room(room_name)
                elif message.startswith('/join'):
                    room_name = message.split(' ')[1]
                    self.join_room(username, room_name)
                elif message.startswith('/leave'):
                    room_name = message.split(' ')[1]
                    self.leave_room(username, room_name)
                elif message.startswith('/quit'):
                    client_socket.send('Goodbye!'.encode('utf-8'))
                    break
                else:
                    self.send_message(username, message)
            except Exception as e:
                print(e)
                break

if __name__ == "__main__":
    server_socket = socket.socket()
    ip = "127.0.0.1"
    port = 8888

    clients = []
    names = {}
    rooms = {}

    chat_app = ChatRoomApp(ip, port, server_socket, names, rooms, clients)
    chat_app.main()
