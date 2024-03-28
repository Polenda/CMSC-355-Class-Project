import socket
import struct
import traceback

class PeerConnection:
    def __init__(self, peerId, host, port, sock = None, debug = False):
        # Raises exceptions which can be handled properly
        self.id = peerId
        self.debug = debug
        
        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock
            
        self.sd = self.s.makefile('rw', 0)
        
    def make_message(self, messageType, messageData):
        # Creates a message
        messageLength = len(messageData)
        message = struct.pack(messageLength, messageType, messageLength, messageData)
        
        return message
    
    
    def send_message(self, messageType, messageData):
        # Sends a message through our peer connection which returns
        # True if successful
        # False if an error occurs
        try:
            message = self.makeMessage(messageType, messageData)
            self.sd.write(message)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return False
        return True
    
    def receive_message(self):
        # Receives a message from a peer connection
        # returns (None, None) if there is an error
        try:
            messageType = self.sd.read(4)
            if not messageType: return (None, None)
            
            lengthStored = self.sd.read(4)
            messageLength = int(struct.unpack("!L", lengthStored)[0])
            message = ""
            
            while len(message) != messageLength:
                data = self.sd.read(min(2048, messageLength - len(message)))
                if not len(data):
                    break
                message += data
                
            if len(message) != messageLength:
                return(None, None)
            
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return(None, None)
        
        return(messageType, message)
    
    def close_peer_connection(self):
        # Closes the peer connection
        # sendData and receiveData methods will not work once closePeerConnection is called
        self.s.close()
        self.s = None
        self.sd = None

    def recvdata(self):
        try:
            msgtype = self.sd.read(4)
            if not msgtype: return (None, None)

            lenstr = self.sd.read(4)
            msglen = int(struct.unpack("!L", lenstr)[0])
            msg = ""

            while len(msg) != msglen:
                data = self.sd.read(min(2048, msglen - len(msg)))
                if not len(data):
                    break
                msg += data

            if len(msg) != msglen:
                return (None, None)

        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return (None, None)

        return (msgtype, msg)