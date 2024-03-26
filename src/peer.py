import sys


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

    def __initserverhost(self):
        pass
