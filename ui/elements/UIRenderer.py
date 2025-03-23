from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .uidrawerinterface import UISurface, UIFont, UISurfaceDrawer
from .uirenderstyle import UIStyle
from .UIFontManager import UIFontManager


Core = TypeVar('Core', bound=Any)

class UIRenderer(Generic[Core], ABC):

    _core: Core # refering UIElement which gets rendered by the Renderer
    def __init__(self, core: Core) -> None:
        self._core = core

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
    _drawer: type[UISurfaceDrawer] | None = None
    _renderstyle: UIStyle | None = None

    @staticmethod
    def init(drawer: type[UISurfaceDrawer], font: type[UIFont], renderstyle: UIStyle) -> None:
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
