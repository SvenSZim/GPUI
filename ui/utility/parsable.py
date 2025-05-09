from abc import ABC, abstractmethod
from typing import Any


class Parsable(ABC):

    @staticmethod
    @abstractmethod
    def parseFromArgs(args: dict[str, Any]) -> 'Parsable':
        pass

