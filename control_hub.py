from interfaces import BionicsInterface
from message_util import Message
"""
================================================================================
CONTROL HUB
================================================================================
A central dispatcher that manages one or more bionic devices ("targets") and
controls which ones are currently receiving messages.

Think of it like a mixing desk: all the devices are plugged in, but you choose
which ones are "live" at any given moment. A message sent through the hub only
reaches the devices you've switched on.

HOW IT WORKS (big picture):
    1. On creation, the hub is given a dictionary of named devices to manage.
          - e.g. { "left_hand": <device>, "right_hand": <device> }

    2. Devices are individually enabled or disabled by name. Only enabled
       devices will receive messages.

    3. connect_all / disconnect_all open and close the connection to every
       registered device at once (regardless of whether they are enabled).

    4. send() delivers a message, of type Message, to every currently-enabled device.
       If no devices are enabled, the message is dropped with a warning.

EXAMPLE:
    hub = ControlHub({"left_hand": left, "right_hand": right})
    hub.connect_all()
    hub.enable("left_hand")
    hub.send(Message(finger=1, curl=128))  # only left_hand receives this
    hub.disconnect_all()

VALID TARGETS:
    Any object that implements BionicsInterface (i.e. has connect, disconnect,
    and send methods). See interfaces.py for the contract.

ADDING A NEW DEVICE:
    Pass it in the targets dictionary at construction time — no other changes
    needed. Then call enable("<name>") before sending messages to it.
================================================================================
"""

class ControlHub:
    def __init__(self, targets: dict[str, BionicsInterface]):
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
    def send(self, message: Message):
        if not self.active:
            print('WARNING: No active targets, message dropped!')
            return
        for name in self.active:
            self.targets[name].send(message)
