from abc import ABC, abstractmethod

class Surface(ABC):
    @abstractmethod
    def blit(self, surface: 'Surface', position: tuple[int, int]) -> None:
        """
        Combines the two surfaces
        """
        pass

class UIRendererInterface(ABC):

    @abstractmethod
    @staticmethod
    def drawline(surface: Surface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: tuple[int, int, int]) -> None:
        pass

    @abstractmethod
    @staticmethod
    def drawrect(surface: Surface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: tuple[int, int, int], fill: bool = True) -> None:
        pass
