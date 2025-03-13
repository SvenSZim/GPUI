
from abc import ABC, abstractmethod


class UISurface(ABC):
    
    @abstractmethod
    def getSize(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def blit(self, surface: 'UISurface', position: tuple[int, int]) -> None:
        """
        Combines the two surfaces
        """
        pass

