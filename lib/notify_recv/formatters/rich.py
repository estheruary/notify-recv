from notify_recv.formatters.base import Formatter

from rich.console import Console

class RichFormatter(Formatter):
    format_str = 'rich'

    def __init__(self):
        self._console = Console(log_path=False)

    def send(self, message):
        urgency = message.hints["urgency"] or 0

        if urgency == 2:
            self._console.log(f"[bold red]{message.app_name}: {message.summary} {message.body}[/bold red]")
        elif urgency == 1:
            self._console.log(f"{message.app_name}: {message.summary} {message.body}")
        else:
            self._console.log(f"[gray]{message.app_name}: {message.summary} {message.body}[/gray]")
