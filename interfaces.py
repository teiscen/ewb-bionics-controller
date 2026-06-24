from abc import ABC, abstractmethod
from message_util import Message, StringConstructor
import socket

# NOTE TO SELF: The controllers need the parser, the interface need the constructor
"""
================================================================================
BIONIC INTERFACES
================================================================================
Defines the contract that any bionic device connection must follow, and provides
a concrete implementation for sending data over a UDP network socket.

HOW IT WORKS (big picture):
    1. BionicsInterface is a blueprint — it declares that every device driver
       MUST implement three actions: connect, disconnect, and send.
       It cannot be used directly; it exists to keep all drivers interchangeable.

    2. UDPInterface is a real implementation of that blueprint. It sends
       messages to a device over the network using the UDP protocol —
       a lightweight, fire-and-forget method of transmission suited to
       frequent, time-sensitive updates like finger position data.

EXAMPLE:
    device = UDPInterface(host="192.168.1.10", port=5005)
    device.connect()
    device.send("finger: 1, curl: 128")
    device.disconnect()

ADDING YOUR OWN CONNECTION TYPE:
    Subclass BionicsInterface and implement the three required methods:
        - connect()        : open the connection to the device
        - disconnect()     : cleanly close it
        - send(message)    : transmit a message string to the device

    The ControlHub will accept any class that follows this contract, so no
    other code needs to change.

    Example (Serial/USB):
        class SerialInterface(BionicsInterface):
            def connect(self):    ...
            def disconnect(self): ...
            def send(self, message): ...
================================================================================
"""

# ---------------------------------------------------------------------------
# BIONIC INTERFACE  (Blueprint)
# Defines the three actions every device driver must support.
# Any class that inherits from this is forced to implement all three —
# the program will refuse to run otherwise.
# ---------------------------------------------------------------------------
class BionicsInterface(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def disconnect(self): pass
    
    @abstractmethod
    def send(self, message: Message): pass

# ---------------------------------------------------------------------------
# UDP INTERFACE  (Network implementation)
# Sends messages to a device over a local or remote network using UDP.
# UDP is connectionless — there is no handshake or delivery confirmation,
# making it fast and simple, but the caller should not assume messages arrive.
# ---------------------------------------------------------------------------
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

    def send(self, message: Message):
            if self.sock:
                match message_string := StringConstructor.construct(message):
                    case None:
                        return 
                    case str():
                        self.sock.sendto(message_string.encode('utf-8'), (self.host, self.port))
                        print(f'[UDP] sent finger={message.finger}, curl={message.curl}')


