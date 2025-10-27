from abc import ABC

from .....utility       import Rect
from .....interaction   import Clickable
from ...elementcore  import ElementCore

class InteractableCore(ElementCore, Clickable, ABC):
    """Core implementation for interactive UI elements managing click behavior.
    
    Combines the functionality of ElementCore for layout/positioning with Clickable
    for mouse interaction handling. This class provides the foundational behavior for:
    - Click detection and handling
    - Button state management
    - Event triggering
    
    Concrete implementations extend this to add specific interactive behaviors
    while maintaining consistent click handling and state management.
    """

    def __init__(self, rect: Rect) -> None:
        ElementCore.__init__(self, rect)
