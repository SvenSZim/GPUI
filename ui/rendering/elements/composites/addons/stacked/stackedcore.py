from typing import Any, override

from ......utility import Rect
from ....element   import Element
from ..addoncore   import AddonCore
from ..grouped     import Grouped

class StackedCore(AddonCore[Element]):
    """
    StackedCore is the core object of the addon 'Stacked'.
    """
    def __init__(self, rect: Rect, elementSizing: Rect, *inner: Element | tuple[Element, float], alignVertical: bool=True, offset: int=0) -> None:
        
        relativeSizing = [1.0 if isinstance(el, Element) else el[1] for el in inner]
        totalSizing = sum(relativeSizing)

        preRect: Rect
        if alignVertical:
            preRect = Rect(rect.getPosition(),
                           (elementSizing.getWidth(),
                            int(elementSizing.getHeight() * totalSizing) + offset * (len(relativeSizing) - 1))
                          )
        else:
            preRect = Rect(rect.getPosition(),
                           (int(elementSizing.getWidth() * totalSizing) + offset * (len(relativeSizing) - 1),
                            elementSizing.getHeight())
                          )
        if totalSizing == 0.0:
            totalSizing = 1.0
        super().__init__(preRect, Grouped(preRect, *[(el, 1.0/totalSizing) if isinstance(el, Element) else (el[0], el[1]/totalSizing) for el in inner], alignVertical=alignVertical, offset=offset))
    
    @override
    def _alignInner(self) -> None:
        self._inner.align(self)
        self._inner.alignSize(self)

    @override
    def getInnerSizing(self, elSize: tuple[int, int], args: dict[str, Any]={}) -> tuple[int, int]:
        return self._inner.getInnerSizing(elSize)
