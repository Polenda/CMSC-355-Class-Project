import json
import socket
import threading
from datetime import datetime


class Server:
    clients: list = []
    nicknames: list = []

    def __init__(self, h, p):
        self.host = h
        self.port = p
        self.socket = None

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen()  # Check for incoming connections
            print(f"ChatServer started with server IP: {self.host}, port: {self.port} ...")
            for i in range(3):  # Separation via three dots as indicated by the example
                print(".")
        except socket.error as _e:
            print(f"ERR - cannot create ChatServer socket using port number '{self.port}'.")

    def broadcast_message(self, message):
        """Display a message to all clients connected to the server."""
        receivers = []
        for client in self.clients:
            # If client is the owner of the message: continue
            client.send(message)
            receivers.append(client)
            # print(Broadcasted: <Client1 Nickname>, <Client2 Nickname>, <Client3 Nickname>)

    def handle(self, client):
        """For each user, a thread is created and is running this method. Checks for user message inputs."""
        while True:
            try:  # Get message from a client
                message = client.recv(1024)
                self.broadcast_message(message)
            except ConnectionError as _e:  # Kick user if unable to do so
                self.disconnect_client(client)
                break
            except socket.error as _e:
                self.disconnect_client(client)
                break

    def disconnect_client(self, client):
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()

        nickname = self.nicknames[index]
        self.nicknames.remove(nickname)

        message: str = f"{get_time()} :: {nickname}: disconnected."
        self.broadcast_message(message.encode('ascii'))     # Tell users
        print(message)                                      # Server log


def receive(serv: Server):
    """Get client connection."""
    while True:
        client, address = serv.socket.accept()
        curr_time = get_time()
        client_info_json: json = client.recv(1024).decode('utf-8')

        try:
            client_info = json.loads(client_info_json)
            nickname = client_info['nickname']

            # TODO: Check if user_name is the same as any existing users; if so then disconnect client
            if nickname in serv.nicknames:  # or user_id in serv.clients:
                client.send("ERR - Username is already taken. Please enter a different one.".encode('ascii'))
                client.close()
                continue

            serv.broadcast_message(f"{nickname} has joined the server\n".encode('ascii'))
            serv.clients.append(client)
            serv.nicknames.append(nickname)

            print(f"{curr_time} :: {nickname}: connected.")
            client.send("Enter message:".encode('ascii'))

            thread = threading.Thread(target=serv.handle, args=(client,))
            thread.start()
        except Exception as _e:
            client.send(f"ERR - Unable to establish connection. Try again later.".encode('ascii'))
            client.close()
            continue


def get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    host: str = '127.0.0.1'
    port: int = 45100

    s: Server = Server(host, port)
    receive(s)
