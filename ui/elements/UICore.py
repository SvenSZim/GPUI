from abc import ABC, abstractmethod

class UICore(ABC):

    @abstractmethod
    def update(self) -> None:
        pass
