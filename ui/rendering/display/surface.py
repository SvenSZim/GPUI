from abc import ABC, abstractmethod


class Surface(ABC):
    """
    Surface is the abstract base class of all surfaces used in the UI.
    It defines some needed functionality which needs to be implemented as interface.
    """
    
    @abstractmethod
    def getSize(self) -> tuple[int, int]:
        """
        getSize return the size of the Surface instance

        Returns (tuple[int, int]): (width, height) ~ the size of the UISurface
        """
        pass

    @abstractmethod
    def blit(self, surface: 'Surface', position: tuple[int, int]) -> None:
        """
        blit merges a given surface onto itself

        Args:
            surface     ('Surface')         : the surface that is to be merged
            position    (tuple[int, int])   : the position where to merge the given surface
                                              onto this surface
        """
        pass

