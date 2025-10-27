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

    __cachedSortedRenderer: list['Renderer'] = []

    _postRenderQueue: list['Renderer'] = []

    @staticmethod
    def init(drawer: type[SurfaceDrawer], font: type[Font]) -> None:
        """
        Initialize renderer globals required for drawing UI elements.

        Args:
            drawer (type[SurfaceDrawer]): drawing backend class used to render surfaces.
            font   (type[Font]): font class implementation to register with FontManager.
        """
        Renderer._drawer = drawer
        FontManager.setFont(font)

    @staticmethod
    def addPostRenderElement(element: 'Renderer') -> None:
        """
        Add an element to be rendered after all normal elements.

        Post-render elements (like tooltips or overlays) are guaranteed to be
        drawn on top of normal elements, regardless of z-index. The queue is
        cleared after each render cycle.

        Args:
            element (Renderer): Element to add to post-render queue
        """
        Renderer._postRenderQueue.append(element)

    @staticmethod
    def _renderPost(screen: Surface) -> None:
        """Render all elements in the post-render queue and clear it.
        
        Internal method called by renderAll() after normal elements are drawn.
        Requires _drawer to be initialized.

        Args:
            screen (Surface): Target surface to render onto
        """
        assert Renderer._drawer is not None
        for el in Renderer._postRenderQueue:
            el.render(screen)
        Renderer._postRenderQueue = []

    @staticmethod
    def renderAll(screen: Surface, elements: list['Renderer']) -> list['Renderer']:
        """
        Render all elements in z-index order followed by post-render elements.

        Elements are sorted by z-index if the list has changed since last render.
        After normal elements are drawn, any elements in the post-render queue
        are rendered on top.

        Args:
            screen (Surface): Target surface to render onto
            elements (list[Renderer]): List of elements to render

        Returns:
            list[Renderer]: The sorted list of elements that were rendered

        Raises:
            ValueError: If renderer was not initialized with a drawer
        """
        if Renderer._drawer is None:
            raise ValueError("Renderer::drawer not instantiated!")
        
        if elements != Renderer.__cachedSortedRenderer:
            elements = sorted(elements, key=lambda x: x.getZIndex())
            Renderer.__cachedSortedRenderer = elements
        for element in elements:
            element.render(screen)

        if len(Renderer._postRenderQueue) > 0:
            Renderer._renderPost(screen)

        return elements
