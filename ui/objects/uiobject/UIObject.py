from typing import override

from ..idrawer import UISurface
from ..uiobjectbody import UIABCBody
from .UIABCObject import UIABCObject



class UIObject(UIABCObject):
    """
    UIObject is a the most basic UI-Object
    It consists just of its body and a boolean which activates or deactivates itself
    """
    
    def __init__(self, objectBody: UIABCBody) -> None:
        """
        __init__ initializes the UIObject instance

        Args:
            objectBody: UIABCBody = the body of the UIObject
        """
        self.body = objectBody
        UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)


from ..UIRenderer import UIRenderer
from ..uistyle import UIStyleElements
from .UIABCObject import UIABCObjectRenderer

class UIObjectRenderer(UIABCObjectRenderer[UIObject]):
    """
    UIObjectRender is the UIElementRender for all UIObjects.
    """

    def __init__(self, body: UIObject | UIABCBody, active: bool=True) -> None:
        """
        __init__ initializes the UIObjectRender instance

        Args:
            body: UIObject | UIABCBody = the refering UIObject (Or UIABCBody bcs. they are 'equivalet')
            active: bool = active-state of the UIObjectRenderer
        """
        if isinstance(body, UIABCBody):
            body = UIObject(body)
        self.body = body
        self.active = active

    @override
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """

        # check if UIElement should be rendered
        if not self.active:
            return


        UIRenderer.getRenderStyle().getStyleElement(UIStyleElements.BASIC_RECT).render(surface, self.getUIObject().getRect())
        """
        # check if borders should be drawn
        borders: tuple[bool, bool, bool, bool] | bool = self.getUIRenderInfo().borders
        if isinstance(borders, bool):
            borders = (borders, borders, borders, borders)
        
        if borders[0]:
            UIRenderer.getDrawer().drawline(screen, (left, top), (right, top), (255,255,255))
        if borders[1]:
            UIRenderer.getDrawer().drawline(screen, (left, top), (left, bottom), (255,255,255)) 
        if borders[2]:
            UIRenderer.getDrawer().drawline(screen, (right, top), (right, bottom), (255,255,255))
        if borders[3]:
            UIRenderer.getDrawer().drawline(screen, (left, bottom), (right, bottom), (255,255,255))
        """