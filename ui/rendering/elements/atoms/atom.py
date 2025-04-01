from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..element         import Element
from .atomcore         import AtomCore
from .atomdata         import AtomData
from .atomcreateoption import AtomCreateOption
from .atomprefab       import AtomPrefab

AtomCls = TypeVar('AtomCls', bound='Atom')

Core         = TypeVar('Core'        , bound=AtomCore        )
RenderData   = TypeVar('RenderData'  , bound=AtomData        )
CreateOption = TypeVar('CreateOption', bound=AtomCreateOption)
Prefab       = TypeVar('Prefab'      , bound=AtomPrefab      )

class Atom(Generic[Core, RenderData, CreateOption, Prefab], Element[Core, RenderData], ABC):
    """
    Atom is the abstract base class for all ui-atom-elements.
    """

    # -------------------- creation --------------------
    
    def __init__(self, core: Core, active: bool, renderData: RenderData) -> None:
        super().__init__(core, renderData, active)

    @staticmethod
    @abstractmethod
    def fromCreateOptions(createOptions: list[CreateOption]) -> AtomCls:
        """
        fromCreateOptions creates the atom-element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (this class): instance of the created atom
        """
        pass

    @staticmethod
    @abstractmethod
    def fromPrefab(prefab: Prefab) -> AtomCls:
        """
        fromPrefab creates the atom-element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (this class): instance of the created atom
        """
        pass
