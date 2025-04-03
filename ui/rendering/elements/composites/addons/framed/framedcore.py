
from typing import override
from ....body    import LayoutManager
from ....element import Element
from ..addoncore import AddonCore

class FramedCore(AddonCore[Element]):
    """
    FramedCore is the core object of the addon 'Framed'.
    """
    def __init__(self, inner: Element) -> None:
        super().__init__(inner.getRect(), inner)

    @override
    def alignInner(self) -> None:
        LayoutManager.addConnection((True, True), self._inner.getCore().getBody(), self.getBody(), (0.0, 0.0), (0.0, 0.0))
