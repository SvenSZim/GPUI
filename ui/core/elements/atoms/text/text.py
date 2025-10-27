from typing import Optional, override

from .....utility import Rect
from .....display import Surface, Font, FontManager
from .....interaction import EventManager

from ...body        import Body
from ..atom             import Atom
from .textcore          import TextCore
from .textdata          import TextData

class Text(Atom[TextCore, TextData]):
    """
    Text

    A lightweight atomic UI element for drawing a single block of text.

    Responsibilities
    - Hold textual content in a `TextCore` and rendering parameters in `TextData`.
    - Maintain a render-cache (surface + position) computed by
      `updateRenderData()` and used by `render()`.
    - Subscribe to layout updates (via `Body.getLayoutUpdateEvent()`) and
      recompute its render cache when layout or data changes.

    Rendering contract
    - `updateRenderData()` computes the surface used to draw the text and
      the top-left position where it should be blitted. It must not perform
      long-running operations and should return quickly.
    - `render(surface)` simply blits the prepared surface if available.

    Color and font handling
    - `TextData.textColor` may be a `tColor` instance, an RGB/RGBA tuple or
      a named/hex string; `Text` will try to pass the value to the active
      `Font` implementation and contains fallbacks to common representations
      (`.rgb` / `.value`) for compatibility with different font backends.

    Notes
    - This class performs lightweight validation in the constructor; heavy
      parsing/validation belongs in `TextData.set` / `parseFromArgs`.
    - Thread-safety: methods are intended to be called from the main UI
      thread. Event subscription is used to trigger updates.
    """

    # -------------------- creation --------------------

    def __init__(self, content: str, renderData: TextData, active: bool=True) -> None:
        if not isinstance(content, str):
            raise TypeError(f'content must be a str, got {type(content)}')
        if not isinstance(renderData, TextData):
            raise TypeError(f'renderData must be a TextData instance, got {type(renderData)}')
        super().__init__(TextCore(content), renderData, active)

        self.__renderCache = None
        EventManager.quickSubscribe(Body.getLayoutUpdateEvent(), self.updateRenderData)

    @override
    def copy(self) -> 'Text':
        return Text(self._core.getContent(), renderData=self._renderData.copy(), active=self.isActive())

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, str]) -> 'Text':
        return Text(args['content'], renderData=TextData.parseFromArgs(args))


    # -------------------- rendering --------------------

    __renderCache: Optional[tuple[Surface, tuple[int, int]]]

    @override
    def updateRenderData(self) -> None:
        """
        Recompute the render cache (surface and blit position) for this
        Text atom.

        Responsibilities:
        - Determine the available rectangle via `getRect()` and apply
          configured insets (absolute or fractional).
        - If dynamic text sizing is enabled, compute `fontSize` so the text
          fits into the available box using `getDynamicFontSize()`.
        - Use the active `Font` implementation to render the text. The
          method attempts the provided color format first and falls back
          to `.rgb`/`.value` attributes for compatibility.
        - Store the resulting `(Surface, (x,y))` tuple in `self.__renderCache`
          so `render()` can blit it.

        The method avoids raising exceptions for transient rendering errors;
        instead it clears the render cache so nothing is drawn.
        """
        self.__renderCache = None
        #calculate render borderbox
        rect: Rect = self.getRect()

        #check for errors in boxsize
        if rect.isZero():
            return
        if rect.width < 0:
            rect = Rect((rect.left + rect.width, rect.top), (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect((rect.left, rect.top + rect.height), (rect.width, -rect.height))
        
        # apply partialInset (support numeric or 2-tuple (float or int))
        def applyPartial(rect: Rect, partialInset: tuple[float, float] | float | tuple[int, int] | int) -> Rect:
            # numeric inset (int or float)
            if isinstance(partialInset, (int, float)):
                inset = int(min(rect.width, rect.height) * float(partialInset)) if isinstance(partialInset, float) else int(partialInset)
                return Rect((rect.left + inset, rect.top + inset), (rect.width - 2 * inset, rect.height - 2 * inset))

            # tuple inset - expect 2 elements
            if isinstance(partialInset, tuple) and len(partialInset) == 2:
                a, b = partialInset
                # if fractional (float) treat as percentage of corresponding dimension
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    if isinstance(a, float) or isinstance(b, float):
                        left = rect.left + int(rect.width * (1.0 - float(a)))
                        top = rect.top + int(rect.height * (1.0 - float(b)))
                        width = int(rect.width * (1.0 - 2 * float(a)))
                        height = int(rect.height * (1.0 - 2 * float(b)))
                        return Rect((left, top), (width, height))
                    else:
                        return Rect((rect.left + int(a), rect.top + int(b)), (rect.width - 2 * int(a), rect.height - 2 * int(b)))

            # unknown format - return rect unchanged
            return rect
        
        globalInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.inset
        rect = applyPartial(rect, globalInset)
        if rect.isZero():
            return

        if self._renderData.dynamicText:
            self._renderData.fontSize = getDynamicFontSize(self._renderData.sysFontName, rect.getSize(), self._core.getContent())

        if self._renderData.textColor is not None and self._renderData.fontSize is not None:
            font: Font = FontManager.getFont().SysFont(self._renderData.sysFontName, self._renderData.fontSize)
            # Attempt to render using the color as provided; on failure, try common fallbacks
            color_param = self._renderData.textColor
            try:
                text_render: Surface = font.render(self._core.getContent(), color_param)
            except Exception:
                # fallback: if tColor instance, try rgb tuple then rgba tuple
                try:
                    if hasattr(color_param, 'rgb'):
                        text_render = font.render(self._core.getContent(), color_param)
                    elif hasattr(color_param, 'value'):
                        text_render = font.render(self._core.getContent(), color_param)
                    else:
                        raise
                except Exception:
                    # Cannot render text with provided color; clear cache and exit
                    self.__renderCache = None
                    return

            text_size: tuple[int, int] = text_render.getSize()
            textPosX: int = int(rect.left + (rect.width - text_size[0]) * self._renderData.fontAlign[0])
            textPosY: int = int(rect.top + (rect.height - text_size[1]) * self._renderData.fontAlign[1])
            self.__renderCache = (text_render, (textPosX, textPosY))


    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UIText onto the given surface

        Args:
            surface (Surface): the surface the UIText should be drawn on
        """
        assert self._drawer is not None

        # check if UIElement should be rendered
        if self._active and self.__renderCache is not None:
            surface.blit(self.__renderCache[0], self.__renderCache[1])

# -------------------------------------------------- helpers --------------------------------------------------

def getDynamicFontSize(font_name: str, box_size: tuple[int, int], text: str) -> int:
    """
    getDynamicFont calculates the maximal fontsize to use for the given SysFont
    to still make the given text fit in the given box

    Args:
        font_name: str = the SysFont name to use
        box_size: tuple[int, int]: the size of the box the text should fit in
        text: str = the text to fit in the box

    Returns:
        int = the maximal fontsize to still fit in the box
    """

    def text_fits_in_box(text_render: Surface) -> bool:
        nonlocal box_size
        text_size: tuple[int, int] = text_render.getSize()
        return (box_size[0] > text_size[0]) and (box_size[1] > text_size[1])

    start_search: int = 0
    end_search: int = min(box_size)
    while start_search < end_search:
        mid_search: int = int((start_search + end_search) / 2)
        
        test_font = FontManager.getFont().SysFont(font_name, mid_search)
        test_render: Surface = test_font.render(text, (255, 255, 255))

        if text_fits_in_box(test_render):
            start_search = mid_search + 1
        else: 
            end_search = mid_search - 1

    return start_search
