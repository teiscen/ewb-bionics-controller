# ----- CONDITIONAL 
# NOTE: Including this file is not mandatory; however, it contains many
#       useful methods used to validate and parse messages. 
#       Including the UDP formatted message expected by the he SimuLink model.
#
class Message:
    # Used to map the words for fingers to their integer representation.
    _FINGERS = {
        'thumb': 0, 'index': 1, 'middle': 2, 'ring' : 3, 'pinky': 4,
    }

    # Given a finger and curl value construct the correct message.
    # 
    # ACUTALLY VALIDATE BEFORE CONSTRUCTING
    # SPLIT THE PRIVATE METHODS INTO VALIDATE 
    @staticmethod
    def construct_message(finger, curl):
        return {'finger': finger, 'curl': curl}

    def _parse_finger(self, value):
        if value in self._FINGERS:
            return self._FINGERS[value]

        try: finger = int(value)
        except ValueError: return None

        if 0 <= finger < 5: return finger
        return None

    def _parse_curl(self, value):
        try: curl = int(value)
        except ValueError: return None

        if -180 < curl < 180: return curl
        return None
    
    def parse_string(self, args):
        finger_text, _, curl_text = args.partition(' ')
        finger = self._parse_finger(finger_text)
        curl   = self._parse_curl(curl_text)

        return self.construct_message(finger, curl) 
