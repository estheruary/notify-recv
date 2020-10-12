from notify_recv.formatters.base import Formatter

import json

class JSONFormatter(Formatter):
    format_str = 'json'

    def send(self, message):
        print(json.dumps(message.__dict__))
