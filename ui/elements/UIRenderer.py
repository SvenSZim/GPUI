from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from ..responsiveness import EventManager
from .uidrawerinterface import UISurface, UIFont, UISurfaceDrawer
from .uirenderstyle import UIStyle
from .UIFontManager import UIFontManager
from .UICore import UICore


Core = TypeVar('Core', bound=UICore)

class UIRenderer(Generic[Core], ABC):

    # -------------------------- static -------------------------------

    _layoutUpdate: str | None = None
    _drawer: type[UISurfaceDrawer] | None = None
    _renderstyle: UIStyle | None = None

    # ------------------------- abstract ------------------------------

    _active: bool # boolean if the renderer is active or not
    _core: Core # refering UIElement which gets rendered by the Renderer
    def __init__(self, core: Core, active: bool = True) -> None:
        
        if UIRenderer._layoutUpdate is None:
            raise ValueError("UIRenderer::layoutUpdate not instantiated!")
        
        self._active = active
        self._core = core
        EventManager.subscribeToEvent(UIRenderer._layoutUpdate, self._core.update)

    def isActive(self) -> bool:
        """
        isActive returns the active-state of the Renderer

        Returns:
            bool = active-state of the Renderer
        """
        return self._active

    def toggleActive(self) -> bool:
        """
        toggleActive toggles the active-state of the Renderer

        Returns:
            bool = new active-state of the Renderer
        """
        self._active = not self._active
        return self._active

    def setActive(self, active: bool) -> None:
        """
        setActive sets the active-state of the Renderer

        Args:
            active: bool = new active-state of the Renderer
        """
        self._active = active

    def update(self) -> None:
        """
        update updates the positioning and sizing of the refering UIElement
        """
        self._core.update()

    @abstractmethod
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIElement onto the given surface

        Args:
            surface: UISurface = the surface the UIElement should be drawn on
        """
        pass

    # --------------------- abstract static ---------------------------

    @staticmethod
    @abstractmethod
    def constructor(*args: Any, **kwargs: Any) -> 'UIRenderer':
        """
        constructor fully creates the UIElement

        Args:
            ...: The necessary arguments to create the core and renderer

        Returns:
            UIRenderer: the created element
        """
        pass

    # -------------------------- static -------------------------------

    @staticmethod
    def init(drawer: type[UISurfaceDrawer], font: type[UIFont], renderstyle: UIStyle) -> None:
        UIRenderer._layoutUpdate = EventManager.createEvent()
        UIRenderer._drawer = drawer
        UIFontManager.setFont(font)
        UIRenderer._renderstyle = renderstyle

    @staticmethod
    def renderAll(screen: UISurface, uiobjectrenderer: list['UIRenderer']) -> None:
        if UIRenderer._drawer is None:
            raise ValueError("UIRenderer::drawer not instantiated!")
        
        if UIRenderer._renderstyle is None:
            raise ValueError("UIRenderer::renderstyle is not instantiated!")

        for uior in uiobjectrenderer:
            uior.render(screen)

    #DEBUG
    @staticmethod
    def updateAll() -> None:
        if UIRenderer._layoutUpdate is None:
            raise ValueError("UIRenderer::layoutUpdate not instantiated!")
        EventManager.triggerEvent(UIRenderer._layoutUpdate)
