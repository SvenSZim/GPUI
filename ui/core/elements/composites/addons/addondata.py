from abc import ABC, abstractmethod

from ...elementdata import ElementData

class AddonData(ElementData, ABC):

    @abstractmethod
    def setZIndex(self, zindex: int) -> None:
        pass
