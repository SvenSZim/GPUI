from abc import ABC

from ..UIRenderer import UIRenderer
from ..UICore import UICore


class UIABCComplexCore(UICore, ABC):

    _core_elements: list[UIRenderer]

    def __init__(self, core_elements: list[UIRenderer]) -> None:
        self._core_elements = core_elements

    
    def getSimpleElements(self) -> list[UIRenderer]:
        return self._core_elements
