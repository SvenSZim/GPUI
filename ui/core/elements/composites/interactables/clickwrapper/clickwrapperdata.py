from dataclasses import dataclass
from typing import Any, override

from ..interactabledata     import InteractableData

@dataclass
class ClickwrapperData(InteractableData):
    """
    ClickwrapperData is the storage class for all render-information
    for the interactable 'Clickwrapper'.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'ClickwrapperData':
        return ClickwrapperData()
