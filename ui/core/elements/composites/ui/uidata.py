from dataclasses import dataclass
from typing import Any, override

from ...elementdata     import ElementData

@dataclass
class UIData(ElementData):
    """Storage class for UI element render information.
    
    Maintains rendering parameters and state for the UI composite element.
    While currently a minimal implementation, this class is designed to be
    extended with additional render-specific data fields as needed.
    
    This class serves as a data container for UI-specific rendering attributes
    that may be added in future implementations.
    """

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'UIData':
        return UIData()
