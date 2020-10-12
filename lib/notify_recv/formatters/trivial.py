from notify_recv.formatters.base import Formatter

class PlainFormatter(Formatter):
    format_str = 'plain'
    def send(self, message):
        print(message)
