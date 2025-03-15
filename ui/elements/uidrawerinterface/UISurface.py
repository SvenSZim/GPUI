
from abc import ABC, abstractmethod


class UISurface(ABC):
    """
    UISurface is the abstract base class of all surfaces used in the UI.
    It defines some needed functionality which needs to be implemented as interface.
    """
    
    @abstractmethod
    def getSize(self) -> tuple[int, int]:
        """
        getSize return the size of the UISurface

        Returns:
            tuple[int, int] = (width, height) ~ the size of the UISurface
        """
        pass

    @abstractmethod
    def blit(self, surface: 'UISurface', position: tuple[int, int]) -> None:
        """
        blit merges a given surface onto itself

        Args:
            surface: 'UISurface' = the surface that is to be merged
            position: tuple[int, int] = the position where to merge the given surface
                                        onto this surface
        """
        pass

