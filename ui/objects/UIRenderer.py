from typing import Callable

from .generic import Color, Rect
from .UIABCRenderer import UIABCRenderer
from .idrawer import UISurface, UIFont, UISurfaceDrawer
from .uistyle import UIStyle


class UIRenderer:

    drawer: UISurfaceDrawer | None = None
    font: UIFont | None = None
    renderstyle: UIStyle | None = None

    @staticmethod
    def init(drawer: UISurfaceDrawer, font: UIFont, renderstyle: UIStyle) -> None:
        UIRenderer.drawer = drawer
        UIRenderer.font = font
        UIRenderer.renderstyle = renderstyle

    @staticmethod
    def getDrawer() -> UISurfaceDrawer:
        if UIRenderer.drawer is None:
            raise ValueError("UIRenderer::drawer is not instantiated!")
        return UIRenderer.drawer

    @staticmethod
    def getFont() -> UIFont:
        if UIRenderer.font is None:
            raise ValueError("UIRenderer::font is not instantiated!")
        return UIRenderer.font

    @staticmethod
    def getRenderStyle() -> UIStyle:
        if UIRenderer.renderstyle is None:
            raise ValueError("UIRenderer::renderstyle is not instantiated!")
        return UIRenderer.renderstyle

    @staticmethod
    def render(screen: UISurface, uiobjectrenderer: list[UIABCRenderer]) -> None:
        for uior in uiobjectrenderer:
            uior.render(screen)