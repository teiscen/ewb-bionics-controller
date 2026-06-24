from typing import Any, Protocol
from dataclasses import dataclass


@dataclass
class Message:
    finger: int
    curl: int

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


class ParserInterface(Protocol):
    @classmethod
    def parse(cls, raw_data: Any) -> Message | None: ... 


class ConstructorInterface(Protocol):
    @classmethod
    def construct(cls, message: Message) -> Any | None: ...


# ----- PARSER IMPLEMENTATIONS -----
class StringParser(Validator):
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
            string in the form of "finger: <int | str>, curl: <int>"

        Returns:
            Dict['finger' <int>, 'curl' <int>] if the message could be parsed.
            None if message couldn't be parsed.
        """
        finger_blk, _, curl_blk = message_string.partition(',') 
        _, _, finger_text = finger_blk.partition(':')
        _, _, curl_text   = curl_blk.partition(':')
        
        finger = cls._parse_finger(finger_text.strip())
        curl   = cls._parse_curl(curl_text.strip())

        if finger is None or curl is None:
            return None

        return Message(finger, curl)


# ----- CONSTRUCTOR IMPLEMENTATIONS -----
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














