from .idrawer import UISurface, UIFont, UISurfaceDrawer
from .uistyle import UIStyle
from .UIFontManager import UIFontManager
from .UIABCRenderer import UIABCRenderer



class UIRenderer:

    __drawer: type[UISurfaceDrawer] | None = None
    __renderstyle: UIStyle | None = None

    @staticmethod
    def init(drawer: type[UISurfaceDrawer], font: type[UIFont], renderstyle: UIStyle) -> None:
        UIRenderer.__drawer = drawer
        UIFontManager.setFont(font)
        UIRenderer.__renderstyle = renderstyle

    @staticmethod
    def render(screen: UISurface, uiobjectrenderer: list[UIABCRenderer]) -> None:
        for uior in uiobjectrenderer:
            uior.render(UIRenderer.__drawer, screen)

    """
    @staticmethod
    def renderStyled(screen: UISurface, uiobjectrenderer: list[UIABCRenderer]) -> None:
        for uior in uiobjectrenderer:
            uior.render(UIRenderer.__drawer, screen, UIRenderer.__renderstyle)
    """
