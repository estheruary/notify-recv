from dataclasses import dataclass

@dataclass
class Notification:
    app_name: str
    app_icon: str
    replaces_id: int
    summary: str
    body: str
    actions: list
    hints: dict
    expire_timeout: int

    @staticmethod
    def frommessage(message):
        return Notification(*message.get_args_list())
