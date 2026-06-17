from message_util import Message
from control_hub import ControlHub
import cmd

class SimulinkMessage(cmd.Cmd):
    # Required for some cmd.Cmd inherited methods.
    intro = 'Manual controller for EWB Bionics simulink hand. Type \'?\' to list commands.'
    prompt = '(bionics)'
    message_help = "<finger> must be one of the following: int ranging from 0 to 4 or 'thumb', 'index', 'middle', 'ring', 'pinky'" \
                   "<curl>   must be an int ranging from -180 to 180"
    
    # NOTE: The controller has a control_hub.
    # It is your controller's responsibility to call `send` on the controller.
    def __init__(self, hub):
        super().__init__()
        self.hub = hub
        self.queue = []
        self.file = None

    def help_send(self):
        print(f'Send message: send <finger> <curl>\n{self.message_help}')

    def do_send(self, args):
        try:
            message = Message().parse_string(args)
        except Exception:
            print('Invalid message! Will not be sent.')
            return 0
        
        if message['finger'] is None or message['curl'] is None:
            print('Invalid message! Will not be sent.')
            return 0
        else:
            message_construct = Message.construct_message(message['finger'], message['curl'])
            self.hub.send(message_construct)
            return 0
    
    def help_add(self):
        print(f'Add to queue: add <finger> <curl>\n{self.message_help}')

    def do_add(self, args):
        try:
            message = Message().parse_string(args)
        except Exception:
            print('Invalid message! Will not be added to queue.')
            return 0
        
        if message['finger'] is None or message['curl'] is None:
            print('Invalid message! Will not be added to queue.')
            return 0
        else:
            self.queue.append(message)
            return 0

    def do_flush(self, args):
        "Flush (send) every message currently in queue: flush"
        for m in self.queue:
            message = Message.construct_message(m['finger'], m['curl'])
            self.hub.send_message(message)
        self.queue.clear()
    
    def do_reset(self, args):
        "Delete every message currently in queue: reset"
        self.queue.clear()

    def do_view(self, args):
        "View every message currently in queue: view"
        for m in self.queue:
            print(f"Finger: {m['finger']}, curl: {m['curl']}")
    
    def do_quit(self, args):
        "Quit the app: quit"
        if self.file:
            self.close()
        return True

    # ----- record and playback 
    # Taken from : https://docs.python.org/3/library/cmd.html
    def do_record(self, args):
        'Save commands to filename: record rose.cmd'
        self.file = open(args, 'w')

    def do_stop(self, args):
        "Stop recording: stop"
        self.close()

    def do_playback(self, args):
        'Playback commands from a file: playback rose.cmd'
        self.close()
        with open(args) as f:
            cmd_list = f.read().splitlines()
        self.cmdqueue.extend(cmd_list) 

    # Executes before the commands are played
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

