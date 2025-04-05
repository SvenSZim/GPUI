from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

from .....utility   import Rect
from ...element     import Element
from ...elementcore import ElementCore

Inner = TypeVar('Inner', bound=Union[Element, list[Element]])

class InteractableCore(Generic[Inner], ElementCore, ABC):

    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
