from abc import ABC, abstractmethod

from .uidrawerinterface import UISurface, UIFont, UISurfaceDrawer
from .uirenderstyle import UIStyle
from .UIFontManager import UIFontManager



class UIRenderer(ABC):

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
    
    @abstractmethod
    def render(self, surface: UISurface) -> None:
        """
        render renders the UIElement onto the given surface

        Args:
            surface: UISurface = the surface the UIElement should be drawn on
        """
        pass
