from abc import ABC, abstractmethod
import socket
import struct
# ----- REQUIRED
# NOTE: If you'd like your 'interface' to work with control_hub,
#       you must inherit and implement the abstract methods in BionicsInterface
#
# I DONT THINK INTERFACE IS THE CORRECT WORDING HERE, SHOULD THINK ABOUT RENAMING

# ----- 
# IMPLEMENTING YOUR OWN INTERFACE:
# 1. create a child class: class YourClass(BionicsInterface)
# 2. implement the connect, disconnect, and send methods.
# 3. you may now pass it to control_hub on creation.
#
class BionicsInterface(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def disconnect(self): pass
    
    @abstractmethod
    def send(self, message): pass


# ----- Implementations on the interface
class MockInterface(BionicsInterface):
    def connect(self):
        print('[mock] connected')

    def disconnect(self):
        print('[mock] disconnected')

    def send(self, message):
        print(f'[mock] finger={message["finger"]} curl={message["curl"]}')

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
            payload = struct.pack('Bh', message['finger'], message['curl'])
            self.sock.sendto(payload, (self.host, self.port))
            print(f'[UDP] sent finger={message["finger"]}, curl={message["curl"]}')