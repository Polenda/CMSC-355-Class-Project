import json
import socket
import threading
import traceback

from src.peerConnection import PeerConnection


class Peer:
    def __init__(self, max_peers: int, serverport: int, my_id=None, serverhost=None):
        self.debug = 0

        self.max_peers = max_peers
        self.serverport = serverport

        if serverhost:
            self.serverhost = serverhost
        else:
            self.__initserverhost()

        if my_id:
            self.my_id = my_id
        else:
            self.my_id = "%s:%d" % (self.serverhost, self.serverport)

        self.peers = {}

        self.shutdown = False

        self.handlers = {}
        self.router = None

    def main(self):
        s = self.make_server_socket(self.serverport)
        s.settimeout(2.0)

        print(f'Server started: {self.my_id} ({self.serverhost}:{self.serverport})')

        while not self.shutdown:
            try:
                print("Listening for incoming connections...")
                client_sock, client_addr = s.accept()
                client_sock.settimeout(None)
                # Create thread for each user that connects
                t = threading.Thread(target=self.__handle_peer, args=(client_sock, ))
                t.start()
            except KeyboardInterrupt:
                self.shutdown = True
                continue
            except:
                if self.debug:
                    traceback.print_exc()
                    continue

        print("Closing server...")
        s.close()

    def __initserverhost(self):
        pass

    def make_server_socket(self, port, backlog=5):
        """Create a socket for the server that listens to peer connections."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s

    def __handle_peer(self, client_sock):
        """Receive data from an individual peer that is connected to the server."""
        print(f"Connected {client_sock.getpeername()}")

        host, port = client_sock.getpeername()
        peer_connection = PeerConnection(None, host, port, client_sock)

        try:
            # Data received from another peer is a json object
            packet: json = client_sock.recv(1024).decode('utf-8')
            data = json.loads(packet)
            print(data['MESSAGE'])

        except KeyboardInterrupt as _e:
            print("ERR - Keyboard interruption")
            raise
        except Exception as e:
            print(f"ERROR: {e}")

        peer_connection.close_peer_connection()

    def send_to_peer(self, peer_id, msg_type, msg_data, wait_reply=True):
        if self.router:
            next_pid, host, port = self.router(peer_id)
        if not self.router or not next_pid:
            print(f"Unable to route {msg_type} to {peer_id}")
            return None
        return self.connect_and_send(host, port, msg_type, msg_data, pid=next_pid, wait_reply=wait_reply)

    def connect_and_send(self, host, port, msg_type, msg_data, pid=None, wait_reply=True):
        msg_reply = []
        try:
            peer_connection = PeerConnection(pid, host, port)
            peer_connection.send_message(msg_type, msg_data)
            print(f"Sent {pid}: {msg_type}")

            if wait_reply:
                one_reply = peer_connection.recvdata()
                while(one_reply != (None, None)):
                    msg_reply.append(one_reply)
                    print(f"Got reply {pid}: {str[msg_reply]}")
            peer_connection.close_peer_connection()
        except KeyboardInterrupt as _e:
            print("ERR - Keyboard interruption")
            raise
        except Exception as e:
            print(f"ERROR: {e}")
        return msg_reply
