from abc import ABC, abstractmethod
import socket
# DELETED MOCK FOR SIMPLICITY AND BECAUSE ITLL PROB BE MOVED class BionicsInterface(ABC): @abstractmethod
#
class BionicsInterface(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def disconnect(self): pass
    
    @abstractmethod
    def send(self, message): pass

# TODO: Test the implementation
class UDPInterface(BionicsInterface):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        print(f'[UDP] read to send to {self.host}:{self.port}') 
        
    def disconnect(self): 
        if self.sock: 
            self.sock.close() 
            self.sock = None
        print('[UDP] disconnected')

    def send(self, message):
            if self.sock:
                self.sock.sendto(message.encode('utf-8'), (self.host, self.port))
                print(f'[UDP] sent finger={message["finger"]}, curl={message["curl"]}')


