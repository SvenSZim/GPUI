
from ....element import Element
from ..addoncore import AddonCore

class FramedCore(AddonCore[Element]):
    """
    FramedCore is the core object of the addon 'Framed'.
    """

    def __init__(self, inner: Element) -> None:
        super().__init__(inner)
