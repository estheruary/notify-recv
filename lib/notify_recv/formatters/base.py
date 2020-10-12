from abc import ABCMeta, abstractmethod

class Formatter(metaclass=ABCMeta):
    @abstractmethod
    def send(self, message):
        pass
