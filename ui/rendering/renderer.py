from abc import ABC, abstractmethod
from typing import Any, TypeVar

from .display import Font, FontManager, Surface, SurfaceDrawer
from .style import RenderStyle

RendererCls = TypeVar('RendererCls', bound='Renderer')

class Renderer(ABC):

    # -------------------------- static -------------------------------

    _drawer: type[SurfaceDrawer] | None = None
    _renderstyle: RenderStyle | None = None

    # ------------------------- abstract ------------------------------

    _active: bool   # boolean if the renderer is active or not
    def __init__(self, active: bool = True) -> None:
        self._active = active

    def isActive(self) -> bool:
        """
        isActive returns the active-state of the Renderer

        Returns (bool): active-state of the Renderer
        """
        return self._active

    def toggleActive(self) -> bool:
        """
        toggleActive toggles the active-state of the Renderer

        Returns (bool): new active-state of the Renderer
        """
        self._active = not self._active
        return self._active

    def setActive(self, active: bool) -> None:
        """
        setActive sets the active-state of the Renderer

        Args:
            active (bool): new active-state of the Renderer
        """
        self._active = active

    @abstractmethod
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        pass

    # --------------------- abstract static ---------------------------

    @staticmethod
    @abstractmethod
    def constructor(*args: Any, **kwargs: Any) -> RendererCls:
        """
        constructor fully creates the UI-Element

        Args:
            ...: The necessary arguments to create the core and renderer

        Returns (Renderer): the created element
        """
        pass

    # -------------------------- static -------------------------------

    @staticmethod
    def init(drawer: type[SurfaceDrawer], font: type[Font], renderstyle: RenderStyle) -> None:
        """
        init initializes the meta info necessary for rendering the UI-Elements on the screen.

        Args:
            drawer      (type[SurfaceDrawer) : the engine to be used for drawing on screen
            font        (type[Font])         : the font-implementation to be used for rendering font
            renderstyle (RenderStyle)        : the render-style to be used for styling UI-Elements
        """
        Renderer._drawer = drawer
        FontManager.setFont(font)
        Renderer._renderstyle = renderstyle

    @staticmethod
    def renderAll(screen: Surface, elements: list['Renderer']) -> None:
        """
        renderAll renders all the given uiobjects onto the given screen.

        Args:
            screen   (Surface)        : the surface to be drawn onto
            elements (list[Renderer]) : the elements to be drawn
        """
        if Renderer._drawer is None:
            raise ValueError("Renderer::drawer not instantiated!")
        
        if Renderer._renderstyle is None:
            raise ValueError("Renderer::renderstyle is not instantiated!")

        for element in elements:
            element.render(screen)
