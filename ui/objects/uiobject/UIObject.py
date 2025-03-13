from dataclasses import dataclass

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


from .UIABCObject import UIABCObjectRenderInfo, UIABCObjectRender


@dataclass
class UIObjectRenderInfo(UIABCObjectRenderInfo):
    """
    UIObjectRenderInfo is the RenderInfo for all UIObjectRender
    """
    pass

class UIObjectRender(UIABCObjectRender[UIObject, UIObjectRenderInfo]):
    """
    UIObjectRender is the UIElementRender for all UIObjects.
    """

    def __init__(self, body: UIObject | UIABCBody, renderInfo: UIObjectRenderInfo) -> None:
        """
        __init__ initializes the UIObjectRender instance

        Args:
            body: UIObject | UIABCBody = the refering UIObject (Or UIABCBody bcs. they are 'equivalet')
            renderInfo: UIObjectRenderInfo = the used renderInfo
        """
        if isinstance(body, UIABCBody):
            body = UIObject(body)
        self.body = body
        self.renderInfo = renderInfo
