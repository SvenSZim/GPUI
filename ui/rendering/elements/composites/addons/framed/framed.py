from typing import override

from ......display   import Surface
from .....createinfo import CreateInfo
from ....element     import Element
from ..addon         import Addon

from .framedcore         import FramedCore
from .frameddata         import FramedData
from .framedcreateoption import FramedCO
from .framedprefab       import FramedPrefab

class Framed(Addon[Element, FramedCore, FramedData, FramedCO, FramedPrefab]):
    
    # -------------------- creation --------------------

    def __init__(self, inner: Element, renderData: FramedPrefab | list[FramedCO] | FramedData=FramedPrefab.BASIC, active: bool = True) -> None:
        assert isinstance(renderData , FramedData)
        super().__init__(inner, renderData, active)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[FramedCO]) -> CreateInfo['Framed']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Framed, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: FramedPrefab) -> CreateInfo['Framed']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Framed, renderData=prefab)

    @staticmethod
    @override
    def _coreFromInner(inner: Element) -> FramedCore:
        return FramedCore(inner)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        pass

