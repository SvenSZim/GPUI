from dataclasses import dataclass

from ..uiobjectbody import UIABCBody
from .UIABCObject import UIABCObject



class UIObject(UIABCObject):
    """
    UIObject is a the most basic UI-Object
    It consists just of its body and a boolean which activates or deactivates itself
    """
    
    def __init__(self, objectBody: UIABCBody, active: bool=True) -> None:
        self.active = active
        self.body = objectBody
        UIABCObject.update(self) #explicitly calls the update function from UIObject (in case it gets overwritten)


from .UIABCObject import UIABCObjectRenderInfo, UIABCObjectRender


@dataclass
class UIObjectRenderInfo(UIABCObjectRenderInfo):
    pass

class UIObjectRender(UIABCObjectRender[UIObject, UIObjectRenderInfo]):

    def __init__(self, body: UIObject, renderInfo: UIObjectRenderInfo) -> None:
        self.body = body
        self.renderInfo = renderInfo
