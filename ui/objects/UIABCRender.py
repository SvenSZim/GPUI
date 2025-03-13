from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from .generic import Rect
from .UIABC import UIABC

B = TypeVar('B', bound=UIABC)

@dataclass
class UIABCRenderInfo(ABC):
    """
    UIABCRenderInfo is the abstract base class for all UIElementRenderInfo
    """
    pass

I = TypeVar('I', bound=UIABCRenderInfo)

class UIABCRender(Generic[B, I], ABC):
    """
    UIABCRender is the abstract base class for all UIElementRenders.
    UIElementRenders consist of the corresponding UIElement and some renderInfo.
    """
    
    body: B
    renderInfo: I

    def setRenderInfo(self, renderInfo: I) -> None:
        """
        setRenderInfo sets the renderInfo of the UIElementRenderInfo

        Args:
            renderInfo: I (bound=UIABCRenderInfo)
        """
        self.renderInfo = renderInfo

    def getUIObject(self) -> B:
        """
        getUIObject returns the corresponding UIObject from the UIElementRender

        Returns:
            B (bound=UIABC): Corresponding UIObject
        """
        return self.body

    def getRect(self) -> Rect:
        """
        getRect returns the rect of the corresponding UIElement

        Returns:
            Rect = the rect of the corresponding UIElement
        """
        return self.getUIObject().getRect()

    def getPosition(self) -> tuple[int, int]:
        """
        getPosition returns the position (top-left-corner) of the corresponding UIElement

        Returns:
            tuple[int, int]: top-left-corner of UIElement
        """
        return self.getRect().getPosition()

    def getSize(self) -> tuple[int, int]:
        """
        getSize returns the size of the corresponding UIElement

        Returns:
            tuple[int, int]: width, height of UIElement
        """
        return self.getRect().getSize()

    def getUIRenderInfo(self) -> I:
        """
        getUIRenderInfo returns the UIRenderInfo of the UIElementRender

        Returns:
            I (bound=UIABCRenderInfo): UIRenderInfo of the UIElementRender
        """
        return self.renderInfo

    def update(self) -> None:
        """
        update updates the positioning and sizing of the UIElement
        """
        self.getUIObject().update()

