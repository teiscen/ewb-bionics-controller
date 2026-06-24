from message_util import CLIStringParser
from control_hub import ControlHub
from message_util import Message
import cmd

"""
================================================================================
CLI CONTROLLER
================================================================================
This is a CLI tool to communicate with the Simulink model, and to demonstrate 
how the program is architected. 

HOW TO USE:
    View progam.py to to view how to intialize this. A tutorial on how to use 
    the CLI controller can be accessed by typing help or ? in the terminal.

NOTE: Please try and refrain from modifying this file. Its intended purpose is 
        to demonstrate how the components work together, allow you to quickly 
        begin controlling the Simulink model, and for quickly testing the 
        various components.
================================================================================
"""



class SimulinkMessage(cmd.Cmd):
    # Required for some cmd.Cmd inherited methods.
    intro = 'Manual controller for EWB Bionics simulink hand. Type \'?\' to list commands.'
    prompt = '(bionics)'
    message_help = "<finger> must be one of the following: int ranging from 0 to 4 or 'thumb', 'index', 'middle', 'ring', 'pinky'" \
                   "<curl>   must be an int ranging from -180 to 180"
                    # ^^^ THIS IS WRONG BE SURE TO FIX

    # NOTE: The controller has a control_hub.
    # It is your controller's responsibility to call `send` on the controller.
    def __init__(self, hub: ControlHub):
        super().__init__()
        self.hub = hub
        self.queue: list[Message] = []
        self.file = None

    def help_send(self):
        print(f'Send message: send <finger> <curl>\n{self.message_help}')

    def do_send(self, args):
            match message := CLIStringParser.parse(args):
                case None:
                    print("The message is invalid and will not be sent.")
                    return 
                case Message():
                    self.hub.send(message)
    
    def help_add(self):
        print(f'Add to queue: add <finger> <curl>\n{self.message_help}')

    def do_add(self, args):
        match message := CLIStringParser.parse(args):
            case None:
                print('Invalid message! Will not be added to queue.')
                return 
            case Message():
                self.queue.append(message)
                
    def do_flush(self, args):
        "Flush (send) every message currently in queue: flush"
        for msg in self.queue:
            self.hub.send(msg)
        self.queue.clear()
    
    def do_reset(self, args):
        "Delete every message currently in queue: reset"
        self.queue.clear()

    def do_view(self, args):
        "View every message currently in queue: view"
        for msg in self.queue:
            print(f"Finger: {msg.finger}, curl: {msg.curl}")
    
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


