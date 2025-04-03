from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..style import RenderStyle
from .elementcreateoption import ElementCreateOption
from .elementprefab import ElementPrefab

ElementDataCls = TypeVar('ElementDataCls', bound='ElementData')

CreateOption = TypeVar('CreateOption', bound=ElementCreateOption)
Prefab = TypeVar('Prefab', bound=ElementPrefab)

class ElementData(Generic[CreateOption, Prefab], ABC):
    """
    ElementData is the abstract base class for all render-related
    information of elements.
    """

    @abstractmethod
    def __add__(self, extraData: tuple[CreateOption, RenderStyle]) -> ElementDataCls:
        pass

    @abstractmethod
    def __mul__(self, extraData: tuple[Prefab, RenderStyle]) -> ElementDataCls:
        pass
