from abc import ABC
from typing import Any, TypeVar, override

from ...element         import Element
from .interactablecore          import InteractableCore
from .interactabledata          import InteractableData

Core         = TypeVar('Core'        , bound=InteractableCore        )
Data         = TypeVar('Data'        , bound=InteractableData        )

class Interactable(Element[Core, Data], ABC):

    def __init__(self, core: Core, renderData: Data, renderActive: bool = True) -> None:
        Element.__init__(self, core, renderData, renderActive)

    # -------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any]) -> None:
        super().set(args)
        for tag, value in args.items():
            match tag:
                case 'setButtonActive':
                    if isinstance(value, bool):
                        self._core.setButtonActive(value)
                    else:
                        raise ValueError('setButtonActive expects a bool')
