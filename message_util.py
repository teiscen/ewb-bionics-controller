from typing import Any, Protocol
from dataclasses import dataclass

"""
================================================================================
FINGER CURL MESSAGE SYSTEM
================================================================================
This module is responsible for sending and receiving information about finger
movements — specifically, WHICH finger is moving and HOW MUCH it is curling.

HOW IT WORKS (big picture):
    1. A "Message" is created, holding two pieces of info:
          - which finger (0=thumb, 1=index, 2=middle, 3=ring, 4=pinky)
          - how much that finger is curling (a number from -256 to 256)

    2. A "Parser" reads incoming text and converts it into a Message object
       so the rest of the program can work with it easily.

    3. A "Constructor" does the opposite — it takes a Message object and
       converts it back into text, ready to be sent over a network connection.

VALID VALUES:
    Fingers : 0–4  (or by name: thumb, index, middle, ring, pinky)
    Curl    : -256 to 256  (negative = extend/open, positive = curl/close)

EXAMPLE:
    Incoming text:  "finger: index, curl: 128"
    → Parser turns this into: Message(finger=1, curl=128)
    → Constructor turns Message(finger=1, curl=128) back into: "finger: 1, curl: 128"

ADDING YOUR OWN FORMAT:
    To support a new format (e.g. JSON, bytes), create two classes:

    1. A Parser  — inherits from Validator, takes your raw format in, returns a Message.
    2. A Constructor — inherits from Validator, takes a Message in, returns your format.

    Rules:
        - Always inherit from Validator (gives you range checks and finger name lookup).
        - Always return None on invalid input, never raise an exception.
        - parse()     must always return a Message (or None).
        - construct() must always accept a Message (or None).

    You do not need to touch any existing code — just add your two new classes.
================================================================================
"""

# ---------------------------------------------------------------------------
# MESSAGE
# A simple container that holds the two key pieces of data we care about:
# which finger, and how curled it is. Think of it like a labelled envelope.
# ---------------------------------------------------------------------------
@dataclass
class Message:
    finger: int
    curl: int

# ---------------------------------------------------------------------------
# VALIDATOR
# A shared "rulebook" that both the Parser and Constructor inherit from.
# Defines what counts as a legal finger number or curl value, and provides
# a lookup table so finger names like "index" map to their number (1).
# ---------------------------------------------------------------------------
class Validator:
    # Used to map the words for fingers to their integer representation.
    _MIN_FINGER_VAL = 0; _MAX_FINGER_VAL = 4
    _MIN_CURL_VAL = -256; _MAX_CURL_VAL = 256
    _FINGERS = {
        'thumb': 0, 'index': 1, 'middle': 2, 'ring' : 3, 'pinky': 4,
    }

    @classmethod
    def _finger_isValid(cls, finger: int) -> bool:
        return cls._MIN_FINGER_VAL <= finger <= cls._MAX_FINGER_VAL 

    @classmethod
    def _curl_isValid(cls, curl: int) -> bool:
        return cls._MIN_CURL_VAL <= curl <= cls._MAX_CURL_VAL 

# ---------------------------------------------------------------------------
# INTERFACES (Contracts / Blueprints)
# These describe the shape that any Parser or Constructor must follow.
# They don't do any work themselves — they just define what methods are
# expected to exist, so different implementations stay interchangeable.
# ---------------------------------------------------------------------------
class ParserInterface(Protocol):
    @classmethod
    def parse(cls, raw_data: Any) -> Message | None: ... 


class ConstructorInterface(Protocol):
    @classmethod
    def construct(cls, message: Message) -> Any | None: ...



# ----- CONSTRUCTOR IMPLEMENTATIONS -----

# ---------------------------------------------------------------------------
# STRING PARSER
# Reads a text string in the format "finger: <name or int>, curl: <int>"
# and converts it into a Message object. Returns None if anything is invalid.
#
# Example input:  "finger: index, curl: 128"
# Example output: Message(finger=1, curl=128)
# ---------------------------------------------------------------------------
class StringConstructor(Validator):
    @classmethod
    def construct(cls, message: Message) -> str | None:
        """Constructs a string message in the expected method for the UDP sockets. 

        Args:
            finger: int
            curl:   int 
        Returns:
            string "finger: <int>, curl: <int>" if valid.
            None if invalid
        """
        if cls._finger_isValid(message.finger) and cls._curl_isValid(message.curl):
            return f"finger: {message.finger}, curl: {message.curl}"
        else: 
            return None



# ----- PARSER IMPLEMENTATIONS -----

# ---------------------------------------------------------------------------
# STRING CONSTRUCTOR
# Does the reverse of StringParser — takes a Message object and builds the
# correctly formatted text string ready to be sent over the network.
#
# Example input:  Message(finger=1, curl=128)
# Example output: "finger: 1, curl: 128"
# ---------------------------------------------------------------------------
class CLIStringParser(Validator):
    @classmethod
    def _parse_finger(cls, finger_value: str) -> int | None:
        if (finger_int := cls._FINGERS.get(finger_value)) is not None:
            return finger_int
        else:
            try:
                finger_int = int(finger_value)
                return finger_int if cls._finger_isValid(finger_int) else None
            except ValueError:
                return None

    @classmethod
    def _parse_curl(cls, curl_val: str) -> int | None:
        try: 
            curl = int(curl_val)
        except ValueError: 
            return None

        return curl if cls._curl_isValid(curl) else None

    @classmethod                            # asks for keyType and valType nothing to do with dict size 
    def parse(cls, message_string: str) -> Message | None:
        """
        Args:
            string in the form of "<int | str> <int>"

        Returns:
            Dict['finger' <int>, 'curl' <int>] if the message could be parsed.
            None if message couldn't be parsed.
        """
        finger_text, _, curl_text = message_string.partition(' ') 
        finger = cls._parse_finger(finger_text.strip())
        curl   = cls._parse_curl(curl_text.strip())

        if finger is None or curl is None:
            return None

        return Message(finger, curl)











