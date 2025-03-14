from .idrawer import UISurface, UIFont, UISurfaceDrawer
from .uistyle import UIABCStyle
from .UIFontManager import UIFontManager
from .UIABCRenderer import UIABCRenderer



class UIRenderer:

    __drawer: type[UISurfaceDrawer] | None = None
    __renderstyle: type[UIABCStyle] | None = None

    @staticmethod
    def init(drawer: type[UISurfaceDrawer], font: type[UIFont], renderstyle: type[UIABCStyle]) -> None:
        UIRenderer.__drawer = drawer
        UIFontManager.setFont(font)
        UIRenderer.__renderstyle = renderstyle

    @staticmethod
    def render(screen: UISurface, uiobjectrenderer: list[UIABCRenderer]) -> None:
        if UIRenderer.__drawer is None:
            raise ValueError("UIRenderer::drawer not instantiated!")
        
        if UIRenderer.__renderstyle is None:
            raise ValueError("UIRenderer::renderstyle is not instantiated!")

        for uior in uiobjectrenderer:
            uior.renderStyled(UIRenderer.__drawer, screen, UIRenderer.__renderstyle)
    
    @staticmethod
    def renderUnstyled(screen: UISurface, uiobjectrenderer: list[UIABCRenderer]) -> None:
        if UIRenderer.__drawer is None:
            raise ValueError("UIRenderer::drawer not instantiated!")

        for uior in uiobjectrenderer:
            uior.render(UIRenderer.__drawer, screen)

