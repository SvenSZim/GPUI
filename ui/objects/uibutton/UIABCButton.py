from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from ..uiobject import UIABCObject



class UIABCButton(UIABCObject, ABC):
    
    @abstractmethod
    def trigger(self) -> None:
        pass

    @abstractmethod
    def addTriggerEvent(self, event: str) -> bool:
        """
        Calls 'testForTrigger' if activated (which could trigger buttonEvent)
        """
        pass

    @abstractmethod
    def addGlobalTriggerEvent(self, event: str) -> bool:
        """
        Triggers buttonEvent if activated
        """
        pass


from ..uiobject import UIABCObjectRenderInfo, UIABCObjectRender

B = TypeVar('B', bound=UIABCButton)

@dataclass
class UIABCButtonRenderInfo(UIABCObjectRenderInfo):
    pass

I = TypeVar('I', bound=UIABCButtonRenderInfo)

class UIABCButtonRender(UIABCObjectRender[B, I], ABC):
    pass
