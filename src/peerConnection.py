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
        
    def makeMessage (self, messageType, messageData):
        # Creates a message
        messageLength = len(messageData)
        message = struct.pack(messageLength, messageType, messageLength, messageData)
        
        return message
    
    
    def sendMessage(self, messageType, messageData):
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
    
    def receiveMessage(self):
        # Receives a message from a peer connection
        # returns (None, None) if there is an error
        try:
            messageType = self.sd.read(4)
            if not messageType: return (None, None)
            
            lengthStored = self.sd.read(4)
            messageLength = int(struct.unpack(lengthStored)[0])
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
    
    def closePeerConnection(self):
        # Closes the peer connection
        # sendData and receiveData methods will not work once closePeerConnection is called
        self.s.close()
        self.s = None
        self.sd = None
            
            
            
    
    
    
        
        