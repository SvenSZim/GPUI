from abc import ABC

from ...elementdata     import ElementData

class InteractableData(ElementData, ABC):
    """Storage class for interactive element render information.
    
    Provides the base data structure for storing rendering parameters specific to
    interactive elements. This class is designed to be extended by concrete
    implementations to add specific rendering data fields needed for different
    types of interactive elements.
    
    While currently minimal, this class establishes the pattern for separating
    interaction state (in Core) from visual state (in Data).
    """
    pass
