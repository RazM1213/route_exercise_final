from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def listen(self, callback):
        pass
