import socket
import threading
import json
from datetime import datetime

import gui

class Client:
    def __init__(self, server_address, server_port, user_name):
        self.address = server_address
        self.port = server_port
        self.username = user_name

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.address, self.port))

            client_info = {
                "type": "nickname",
                "nickname": self.username,
                "timestamp": get_time(),
            }
            client_info_json = json.dumps(client_info)
            self.client.send(client_info_json.encode('utf-8'))

            print(f"ChatClient started with server IP: {self.address}, port: {self.port}, nickname: {self.username}, client ID: {self.id}")

            self.gui = gui
            
        except Exception as e:
            print(f"\nERR - Unable to connect: {e}")

    def receive(self):
        while True:
            try:  # Get message from server
                message = self.client.recv(1024).decode('ascii')
                print(f"{message}")
            except socket.error as _e:
                print("Error occurred in getting message from server")
                self.client.close()
                break

    def write(self):
        """Get user message to send to server"""
        while True:
            message = input("> ")
            packet = f"{get_time()} :: {self.username}: {message}"
            self.client.send(packet.encode('ascii'))


def get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    while True:
        username: str = input("> Enter your username: ")
        if not 13 > len(username) > 0:
            print("Please enter a username of at most 12 characters.\n")
            continue
        if not username.isalnum():
            print("Please use alphanumeric characters (no special characters.)\n")
            continue
        break

    address: str = input("> Server IP address: ")         # 127.0.0.1
    port: int = int(input("> Server port number: "))      # 45100

    client = Client(address, port, username)

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    write_thread = threading.Thread(target=client.write)
    write_thread.start()
