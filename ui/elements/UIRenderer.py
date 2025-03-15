from abc import ABC, abstractmethod

from .uidrawerinterface import UISurface, UIFont, UISurfaceDrawer
from .uirenderstyle import UIABCStyle
from .UIFontManager import UIFontManager



class UIRenderer(ABC):

    __drawer: type[UISurfaceDrawer] | None = None
    __renderstyle: type[UIABCStyle] | None = None

    @staticmethod
    def init(drawer: type[UISurfaceDrawer], font: type[UIFont], renderstyle: type[UIABCStyle]) -> None:
        UIRenderer.__drawer = drawer
        UIFontManager.setFont(font)
        UIRenderer.__renderstyle = renderstyle

    @staticmethod
    def renderAll(screen: UISurface, uiobjectrenderer: list['UIRenderer']) -> None:
        if UIRenderer.__drawer is None:
            raise ValueError("UIRenderer::drawer not instantiated!")
        
        if UIRenderer.__renderstyle is None:
            raise ValueError("UIRenderer::renderstyle is not instantiated!")

        for uior in uiobjectrenderer:
            uior.renderStyled(UIRenderer.__drawer, screen, UIRenderer.__renderstyle)
    
    @staticmethod
    def renderAllUnstyled(screen: UISurface, uiobjectrenderer: list['UIRenderer']) -> None:
        if UIRenderer.__drawer is None:
            raise ValueError("UIRenderer::drawer not instantiated!")

        for uior in uiobjectrenderer:
            uior.render(UIRenderer.__drawer, screen)


    @abstractmethod
    def renderStyled(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, renderStyle: type[UIABCStyle]) -> None:
        """
        renderStyled renders the UIElement with the given style onto the given surface.

        Args:
            surfaceDrawer: UISurfaceDrawer = the drawer to use when drawing on the surface
            surface: UISurface = the surface the UIElement should be drawn on
            renderStyle: UIStyle = the renderstyle used to render
        """
        pass

    @abstractmethod
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface) -> None:
        """
        render renders the UIElement onto the given surface

        Args:
            surfaceDrawer: UISurfaceDrawer = the drawer to use when drawing on the surface
            surface: UISurface = the surface the UIElement should be drawn on
        """
        pass
