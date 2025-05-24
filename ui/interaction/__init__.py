"""
Initializes the interaction module:
Consists of Event and Input related functionality.
"""

from .event        import EventManager
from .inputevent   import InputEvent
from .inputmanager import InputHandler, InputManager
from .clickables   import Clickable, Holdable, Togglable
