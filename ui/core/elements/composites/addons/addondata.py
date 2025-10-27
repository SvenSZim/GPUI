from abc import ABC, abstractmethod

from ...elementdata import ElementData

class AddonData(ElementData, ABC):
    """Storage class for addon element render information.
    
    Provides the base structure for storing rendering parameters
    specific to addon elements. Implementations add fields needed
    for their specific rendering requirements like:
    - Visual modification data
    - Layout arrangement information
    - State-specific render parameters
    
    This class establishes the pattern for separating addon behavior
    from visual representation data.
    """

    @abstractmethod
    def setZIndex(self, zindex: int) -> None:
        pass
