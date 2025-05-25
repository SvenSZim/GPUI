from abc import ABC, abstractmethod
from typing import TypeVar

from ..display import Font, FontManager, Surface, SurfaceDrawer

RendererCls = TypeVar('RendererCls', bound='Renderer')

class Renderer(ABC):

    # -------------------- creation --------------------

    _active: bool   # boolean if the renderer is active or not
    _zIndex: int    # zIndex of the element (depth)

    def __init__(self, active: bool = True) -> None:
        self._active = active
        self._zIndex = 0

    # -------------------- active-state --------------------

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

    def getZIndex(self) -> int:
        """
        getZIndex returns the z-index of the Renderer
        """
        return self._zIndex

    def setZIndex(self, zindex: int) -> None:
        """
        setZIndex sets the z-index of the Renderer
        """
        self._zIndex = zindex

    # -------------------- abstract-methods --------------------

    @abstractmethod
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        pass

    # #################### CLASS-METHODS ####################

    _drawer: type[SurfaceDrawer] | None = None
    _renderstyle: str = ''

    __cachedSortedRenderer: list['Renderer'] = []

    __postRenderQueue: list['Renderer'] = []

    @staticmethod
    def init(drawer: type[SurfaceDrawer], font: type[Font], renderstyle: str='') -> None:
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
    def addPostRenderElement(element: 'Renderer') -> None:
        """
        addPostRenderElement adds a element to the post-render-queue of the renderer.
        Thereby the element get forcefully rendered after all 'normal' renders.
        """
        Renderer.__postRenderQueue.append(element)

    @staticmethod
    def __renderPost(screen: Surface) -> None:
        assert Renderer._drawer is not None and Renderer._renderstyle is not None
        for el in Renderer.__postRenderQueue:
            el.render(screen)
        Renderer.__postRenderQueue = []

    @staticmethod
    def renderAll(screen: Surface, elements: list['Renderer']) -> list['Renderer']:
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
        
        if elements != Renderer.__cachedSortedRenderer:
            elements = sorted(elements, key=lambda x: x.getZIndex())
            Renderer.__cachedSortedRenderer = elements
        for element in elements:
            element.render(screen)

        if len(Renderer.__postRenderQueue) > 0:
            Renderer.__renderPost(screen)

        return elements
