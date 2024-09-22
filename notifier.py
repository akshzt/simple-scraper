from abc import ABC, abstractmethod

class NotifierInterface(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass

class ConsoleNotifier(NotifierInterface):
    def notify(self, message: str):
        print(message)
