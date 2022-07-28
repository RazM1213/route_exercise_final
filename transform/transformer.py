from abc import ABC, abstractmethod
from models.output import Output


class Transformer(ABC):

    @abstractmethod
    def parse_output(self, json_input) -> Output:
        pass
