from dataclasses import dataclass

# ----- CONDITIONAL 
# NOTE: Including this file is not mandatory; however, it contains many
#       useful methods used to validate and parse messages. 
#       Including the UDP formatted message expected by the he SimuLink model.
#

@dataclass
class message:
    finger: int
    curl:   int

class MessageUtil:
    # Used to map the words for fingers to their integer representation.
    _MIN_CURL_VAL = -127; _MAX_CURL_VAL = 127
    _MIN_FINGER_VAL = 0; _MAX_FINGER_VAL = 4 #Should honestly be assigned from _FINGERS
    _FINGERS = {
        'thumb': 0, 'index': 1, 'middle': 2, 'ring' : 3, 'pinky': 4,
    }

    # Given a finger and curl value construct the correct message.
    # 
    @staticmethod
    def construct_message(finger: int, curl: int) -> str:
        """Constructs a message in the form of the expected string.
            This is how the UDP sockets expect the message to be formatted, 
            so it is better for you to use this method as opposed to defining your own (if possible).
        """
        return f"Finger: {finger}, Curl {curl}"


    @classmethod
    def _parse_finger(cls, value):
        if value in cls._FINGERS:
            return cls._FINGERS[value]

        try: 
            finger = int(value)

            if cls._MIN_FINGER_VAL <= finger <= cls._MAX_FINGER_VAL:
                return finger
            else:
                return None

        except ValueError: 
            print("Could not parse finger.") 
            return None

    @classmethod
    def _parse_curl(cls, value):
        try:
            curl = int(value)
        except ValueError:
            print("Could not parse curl")
            return None

        if cls._MIN_CURL_VAL <= curl <= cls._MAX_CURL_VAL:
            return curl
        else:
            return None

    @classmethod 
    def parse_string(cls, message_str: str) -> dict[str, int] | None:
        """Intended to parse message strings. Check if return is None.

        Args:
            message_str: Expected form "Finger: <str | int>, Curl: <int>".

        Returns:
            A dict containing the int value of 'finger' and 'curl' or None if parsing failed.
        """
        finger_temp, _, curl_temp = message_str.partition(',')
        _, _, finger_text = finger_temp.partition(':')
        _, _, curl_text   = curl_temp.partition(':')
        finger_text.strip()
        curl_text.strip()

        try:
            finger_int = cls._parse_finger(finger_text)
            curl_int   = cls._parse_curl(curl_text) 

            if finger_int is None or curl_int is None:
                return None
            else:
                return {"finger": finger_int, "curl": curl_int}

        except Exception:
            return None
        
























