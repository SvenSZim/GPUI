from abc import ABC
from typing import Generic, TypeVar, Union

from .....utility   import Rect
from ...element     import Element
from ...elementcore import ElementCore

Inner = TypeVar('Inner', bound=Union[Element, list[Element]])

class AddonCore(Generic[Inner], ElementCore, ABC):

    _inner: Inner

    def __init__(self, outer: Rect, inner: Inner) -> None:
        super().__init__(outer)
        self._inner = inner

    def getInner(self) -> Inner:
        return self._inner
