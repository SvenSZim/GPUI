

from abc import ABC, abstractmethod


class UIABCBody(ABC):

    position: tuple[int | float, int | float]
    size: tuple[int | float, int | float]

    topleft: tuple[int, int]
    width: int
    height: int

    @abstractmethod
    def getPosition(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def getSize(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
