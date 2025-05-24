from dataclasses import dataclass
from typing import Any, override

from ..interactabledata     import InteractableData

@dataclass
class TogglewrapperData(InteractableData):
    """
    TogglewrapperData is the storage class for all render-information
    for the interactable 'Togglewrapper'.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'TogglewrapperData':
        return TogglewrapperData()
