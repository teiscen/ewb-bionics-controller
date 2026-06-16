from abc import ABC, abstractmethod
import socket
import struct

# ----- REQUIRED
# 
# YOUR PROGRAM MUST:
#   1. initialize the interface and add them upon creating a ControlHub object.
#   2. enable the interfaces using `enable`
#   3. connect all the interface with `connect_all` 
#   4. diconnect all the interfaces with `disconnect_all`
#   NOTE: Go to example/program.py (ctrl+f "hub") to view an implementation
#
class ControlHub:
    def __init__(self, targets: dict[str, BisonicsInterface]):
        self.targets = targets
        self.active = set()

        if not targets:
            print('WARNING: No targets registered!')

    def enable(self, name: str):
        if name in self.targets:
            self.active.add(name)
        else:
            print(f'WARNING: Unknown target "{name}"')

    def disable(self, name: str):
        self.active.discard(name)

    def connect_all(self):
        for target in self.targets.values():
            target.connect()

    def disconnect_all(self):
        for target in self.targets.values():
            target.disconnect()
            
    # Instructs every interface in `target` (configured with `enable`) to send a message
    def send(self, message):
        if not self.active:
            print('WARNING: No active targets, message dropped!')
            return
        for name in self.active:
            self.targets[name].send(message)
