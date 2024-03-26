import json
import socket
import threading
import traceback


class Peer:
    def __init__(self, max_peers: int, serverport, my_id=None, serverhost=None):
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

        # host, port = client_sock.getpeername()
        # TODO: Create a PeerConnection class. Look at cs.berry.edu's btpeer.py for the example
        # peer_connection = PeerConnection(None, host, port, client_sock)

        while True:
            try:
                # Data received from another peer is a json object
                packet: json = client_sock.recv(1024).decode('utf-8')
                data = json.loads(packet)
                print(data['MESSAGE'])

            except ConnectionError as _e:
                pass
