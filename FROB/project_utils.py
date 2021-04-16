import re

mobile_validation = lambda mobile_number: bool(re.search(r"^[9876]\d{9}$", str(mobile_number)))


class CustomMessage(Exception):
    def __init__(self, message):
        self.message = message
