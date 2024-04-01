import sys
import socket
import threading
import json
from datetime import datetime


# TODO: Packet structure between client and server should be this. Not a single string line
# message_packet = {
#     'type': 'message',        # initial packet when the user joins the server should be nickname
#     'nickname': username,
#     'message': message,
#     'timestamp': get_time(),
# }


class Client:
    def __init__(self, server_address, server_port, username, user_id):
        self.address = server_address
        self.port = server_port
        self.username = username
        self.id = user_id

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.address, self.port))

            client_info = {
                "type": "nickname",
                "nickname": self.username,
                "clientID": self.id,
                "timestamp": get_time(),
            }
            client_info_json = json.dumps(client_info)
            self.client.send(client_info_json.encode('utf-8'))

            print(f"ChatClient started with server IP: {self.address}, port: {self.port}, nickname: {self.username}, client ID: {self.id}")
        except Exception as e:
            print(f"ERR - Unable to connect: {e}")

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
            message = input()
            packet = f"{get_time()} :: {self.username}: {message}"
            self.client.send(packet.encode('ascii'))


def get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    # > python ChatClient.py 127.0.0.1 45100 Josh 001
    address: str = sys.argv[1]  # '127.0.0.1'
    port: int = int(sys.argv[2])  # 45100
    client_name: str = sys.argv[3]
    client_id: int = int(sys.argv[4])
    # TODO: Detect for missing args (ERR - arg x (x indicates missing arg number))

    client = Client(address, port, client_name, client_id)

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    write_thread = threading.Thread(target=client.write)
    write_thread.start()
