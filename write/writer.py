from abc import ABC, abstractmethod


class Writer(ABC):

    @abstractmethod
    def write(self, output):
        pass
