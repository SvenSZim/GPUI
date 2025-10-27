from typing import Any, Optional, override
from math import sqrt

from .....utility import Rect, Color
from .....display import Surface
from .....interaction import EventManager

from ...body    import Body
from ..atom             import Atom
from .linecore          import LineCore
from .linedata          import LineData, AltMode

class Line(Atom[LineCore, LineData]):
    """UI element for drawing lines and line patterns.

    Features:
    - Single or multi-segment lines
    - Pattern support with ordered sections
    - Cross pattern rendering
    - Variable thickness
    - Color patterns
    - Flip/mirror support
    - Inset control

    Attributes:
        __renderCache: Cached line segments for efficient rendering

    Thread Safety:
    - Render cache updates are synchronized
    - Property updates are thread-safe
    - Event handling is synchronized
    """

    def __init__(self, renderData: LineData, active: bool = True) -> None:
        """Initialize a line element.

        Args:
            renderData: Line visual properties
            active: Initial visibility state

        Raises:
            TypeError: If renderData is not LineData
            ValueError: If renderData is invalid
        """
        if not isinstance(renderData, LineData):
            raise TypeError(f'renderData must be LineData, got {type(renderData)}')
            
        # Initialize base with default core
        super().__init__(LineCore(), renderData, active)
        
        # Initialize render cache and subscribe to updates
        self.__renderCache: list[tuple[Rect | tuple[tuple[int, int], 
                                               tuple[int, int], int], Color]] = []
        EventManager.quickSubscribe(
            Body.getLayoutUpdateEvent(), self.updateRenderData)

    @override
    def copy(self) -> 'Line':
        return Line(renderData=self._renderData.copy(), active=self.isActive())

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'Line':
        """Create a Line instance from argument dictionary.

        Args:
            args: Property dictionary with required fields:
                - color: Line color
                - thickness: Line width
                Optional fields:
                - pattern: Line pattern specification
                - inset: Edge insets
                - flip: Mirror flag

        Returns:
            New Line instance

        Raises:
            TypeError: If args is not a dictionary
            ValueError: If required args are missing
        """
        if not isinstance(args, dict):
            raise TypeError(f'args must be dictionary, got {type(args)}')

        # Parse render data and create line
        return Line(renderData=LineData.parseFromArgs(args))

    # -------------------- rendering --------------------

    __renderCache: list[tuple[Rect | tuple[tuple[int, int], tuple[int, int], int], Color]]

    def _calculate_step_size(self, step: int | float, rect: Rect,
                             whratio: float, normalizer: float) -> tuple[float, float]:
        """Calculate step sizes for line segments.

        Args:
            step: Step size (absolute or relative)
            rect: Bounding rectangle
            whratio: Width/height ratio
            normalizer: Normalization factor

        Returns:
            tuple[float, float]: X and Y step sizes
        """
        if isinstance(step, float):
            return (rect.width * step, rect.height * step)
        else:
            return (step * whratio * normalizer if rect.width > 0 else 0,
                    step * normalizer if rect.height > 0 else 0)

    def _get_section_properties(self, section: str) -> tuple[Optional[Color], int, AltMode]:
        """Get properties for a line section.

        Args:
            section: Section identifier

        Returns:
            tuple: (color, thickness, altmode) for section
        """
        default = ''
        return (
            self._renderData.colors[section] \
                if section in self._renderData.colors \
                else self._renderData.colors[default],
            self._renderData.thickness[section] \
                if section in self._renderData.thickness \
                else self._renderData.thickness[default],
            self._renderData.altmode[section] \
                if section in self._renderData.altmode \
                else self._renderData.altmode[default]
        )

    @override
    def updateRenderData(self) -> None:
        """Update cached line segments for rendering.

        Calculates line segments based on:
        - Current rectangle bounds
        - Line pattern specification
        - Section properties (color, thickness, mode)
        """
        # Clear existing cache
        self.__renderCache = []

        # Get and validate bounds
        rect: Rect = self.getRect()

        # Validate rectangle
        if not rect.isValid() or rect.isZero():
            return

        # Normalize negative dimensions
        if rect.width < 0:
            rect = Rect(
                (rect.left + rect.width, rect.top),
                (-rect.width, rect.height))
        if rect.height < 0:
            rect = Rect(
                (rect.left, rect.top + rect.height),
                (rect.width, -rect.height))

        def applyPartial(rect: Rect, 
                         partialInset: tuple[float, float] | float | tuple[int, int] | int
                         ) -> Rect:
            """Apply insets to rectangle.

            Args:
                rect: Rectangle to inset
                partialInset: Inset specification

            Returns:
                New inset rectangle

            Raises:
                ValueError: If inset values are invalid
            """
            if not isinstance(partialInset, (tuple, float, int)):
                raise ValueError(f'Invalid inset type: {type(partialInset)}')

            if isinstance(partialInset, tuple):
                if not len(partialInset) == 2:
                    raise ValueError(
                        f'Inset tuple must have 2 values, got {len(partialInset)}')

                if isinstance(partialInset[0], float):
                    # Percentage insets
                    if not (0 <= partialInset[0] <= 0.5 and \
                           0 <= partialInset[1] <= 0.5):
                        raise ValueError(
                            f'Percentage insets must be between 0-0.5, '
                            f'got {partialInset}')

                    return Rect(
                        (rect.left + int(rect.width * partialInset[0]),
                         rect.top + int(rect.height * partialInset[1])),
                        (int(rect.width * (1.0 - 2 * partialInset[0])),
                         int(rect.height * (1.0 - 2 * partialInset[1]))))
                else:
                    # Absolute insets
                    if not isinstance(partialInset[1], int):
                        raise ValueError(
                            f'Absolute insets must be integers, '
                            f'got {type(partialInset[1])}')

                    insetX = min(partialInset[0], int(rect.width * 0.5))
                    insetY = min(partialInset[1], int(rect.height * 0.5))
                    return Rect(
                        (rect.left + insetX, rect.top + insetY),
                        (rect.width - 2 * insetX, rect.height - 2 * insetY))
            else:
                # Convert single value to tuple
                return applyPartial(rect, (partialInset, partialInset))
        
        globalInset: tuple[float, float] | float | tuple[int, int] | int = self._renderData.inset
        rect = applyPartial(rect, globalInset)
            
        sectionOrder: list[str] = self._renderData.order
        if len(sectionOrder) == 0:
            sectionOrder = ['']

        orderIndex: int = 0

        JIGGLE: int = max(1, int(0.003 * max(rect.width, rect.height)))
        whratio: float = rect.width/rect.height if rect.height > 0 else 1
        absNormalizer: float = 1/sqrt(1 + whratio*whratio) if rect.height > 0 and rect.width > 0 else 1

        nextStep: int | float = self._renderData.sizes[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.sizes else self._renderData.sizes['']
        stepSizeX: float
        stepSizeY: float
        if isinstance(nextStep, float):
            stepSizeX = rect.width*nextStep
            stepSizeY = rect.height*nextStep
        else:
            stepSizeX = nextStep*whratio*absNormalizer if rect.width > 0 else 0
            stepSizeY = nextStep*absNormalizer if rect.height > 0 else 0

        cline: list[float] = [float(x) for x in rect.getPosition()]
        color: Optional[Color]
        thickness: int
        altmode: AltMode
        while rect.collidepoint((int(cline[0] + stepSizeX), int(cline[1] + stepSizeY))):
            color = self._renderData.colors[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.colors else self._renderData.colors['']
            thickness = self._renderData.thickness[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.thickness else self._renderData.thickness['']
            altmode = self._renderData.altmode[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.altmode else self._renderData.altmode['']
            match altmode:
                case AltMode.CROSS:
                    if color is not None:
                        if rect.width > JIGGLE and rect.height > JIGGLE:
                            if self._renderData.flip:
                                self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                                self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1])), thickness), color))
                            else:
                                self.__renderCache.append((((int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), thickness), color))
                                self.__renderCache.append((((int(cline[0]), int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX), int(cline[1])), thickness), color))
                        else:
                            if rect.width > JIGGLE:
                                pJIGGLE = JIGGLE - rect.height
                                if self._renderData.flip:
                                    self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])             + pJIGGLE), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY) - pJIGGLE), thickness), color))
                                    self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1] + stepSizeY) - pJIGGLE), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1])             + pJIGGLE), thickness), color))
                                else:
                                    self.__renderCache.append((((int(cline[0]), int(cline[1])             + pJIGGLE), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY) - pJIGGLE), thickness), color))
                                    self.__renderCache.append((((int(cline[0]), int(cline[1] + stepSizeY) - pJIGGLE), (int(cline[0] + stepSizeX), int(cline[1])             + pJIGGLE), thickness), color))
                            elif rect.height > JIGGLE:
                                pJIGGLE = JIGGLE - rect.width
                                if self._renderData.flip:
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX) + pJIGGLE, rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom + rect.top - int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX) + pJIGGLE, rect.bottom + rect.top - int(cline[1])), thickness), color))
                                else:
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, int(cline[1])), (int(cline[0] + stepSizeX) + pJIGGLE, int(cline[1] + stepSizeY)), thickness), color))
                                    self.__renderCache.append((((int(cline[0]) - pJIGGLE, int(cline[1] + stepSizeY)), (int(cline[0] + stepSizeX) + pJIGGLE, int(cline[1])), thickness), color))
                            else:
                                if self._renderData.flip:
                                    self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                                else:
                                    self.__renderCache.append((((int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), thickness), color))
                case _:
                    if color is not None:
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (int(cline[0] + stepSizeX), rect.bottom + rect.top - int(cline[1] + stepSizeY)), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1])), (int(cline[0] + stepSizeX), int(cline[1] + stepSizeY)), thickness), color))
            cline[0] += stepSizeX
            cline[1] += stepSizeY
            orderIndex = (orderIndex + 1) % len(sectionOrder)
            nextStep = self._renderData.sizes[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.sizes else self._renderData.sizes['']
            stepSizeX: float
            stepSizeY: float
            if isinstance(nextStep, float):
                stepSizeX = rect.width*nextStep
                stepSizeY = rect.height*nextStep
            else:
                stepSizeX = nextStep*whratio*absNormalizer if rect.width > 0 else 0
                stepSizeY = nextStep*absNormalizer if rect.height > 0 else 0

        color = self._renderData.colors[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.colors else self._renderData.colors['']
        thickness = self._renderData.thickness[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.thickness else self._renderData.thickness['']
        altmode = self._renderData.altmode[sectionOrder[orderIndex]] if sectionOrder[orderIndex] in self._renderData.altmode else self._renderData.altmode['']
        match altmode:
            case AltMode.CROSS:
                if color is not None:
                    if rect.width > JIGGLE and rect.height > JIGGLE:
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (rect.right, rect.top), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.top), (rect.right, rect.bottom + rect.top - int(cline[1])), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1])), (rect.right, rect.bottom), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.bottom), (rect.right, int(cline[1])), thickness), color))
                    elif rect.width > JIGGLE:
                        pJIGGLE = JIGGLE - rect.height
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1]) + pJIGGLE), (rect.right, rect.top - pJIGGLE), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.top - pJIGGLE), (rect.right, rect.bottom + rect.top - int(cline[1]) + pJIGGLE), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1]) + pJIGGLE), (rect.right, rect.bottom - pJIGGLE), thickness), color))
                            self.__renderCache.append((((int(cline[0]), rect.bottom - pJIGGLE), (rect.right, int(cline[1]) + pJIGGLE), thickness), color))
                    elif rect.height > JIGGLE:
                        pJIGGLE = JIGGLE - rect.width
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom + rect.top - int(cline[1])), (rect.right + pJIGGLE, rect.top), thickness), color))
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.top), (rect.right + pJIGGLE, rect.bottom + rect.top - int(cline[1])), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, int(cline[1])), (rect.right + pJIGGLE, rect.bottom), thickness), color))
                            self.__renderCache.append((((int(cline[0]) - pJIGGLE, rect.bottom), (rect.right + pJIGGLE, int(cline[1])), thickness), color))
                    else:
                        if self._renderData.flip:
                            self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (rect.right, rect.top), thickness), color))
                        else:
                            self.__renderCache.append((((int(cline[0]), int(cline[1])), (rect.right, rect.bottom), thickness), color))
            case _:
                if color is not None:
                    if self._renderData.flip:
                        self.__renderCache.append((((int(cline[0]), rect.bottom + rect.top - int(cline[1])), (rect.right, rect.top), thickness), color))
                    else:
                        self.__renderCache.append((((int(cline[0]), int(cline[1])), (rect.right, rect.bottom), thickness), color))

    def _validate_render_state(self) -> bool:
        """Validate line state for rendering.

        Checks:
        1. Render data consistency
        2. Cache validity
        3. Core state

        Returns:
            bool: True if line can be rendered
        """
        try:
            if not self._active:
                return False

            if self._drawer is None:
                return False

            if not isinstance(self._renderData, LineData):
                return False

            rect = self.getRect()
            if rect.isZero() or not rect.isValid():
                return False

            return True
        except Exception:
            return False

    @override
    def render(self, surface: Surface) -> None:
        """Render the line onto the given surface.

        Args:
            surface: Target surface for drawing

        Raises:
            ValueError: If surface is invalid
            RuntimeError: If line state is invalid
        """
        if not isinstance(surface, Surface):
            raise ValueError(f'surface must be Surface, got {type(surface)}')

        if not self._validate_render_state():
            return

        if self._drawer is None:
            raise RuntimeError('No drawer available for rendering')

        # Only render if active and cache exists
        if not self._active or not self.__renderCache:
            return

        try:
            for obj, color in self.__renderCache:
                if isinstance(obj, Rect):
                    # Draw rectangle segment
                    self._drawer.drawrect(surface, obj, color)
                elif isinstance(obj, tuple):
                    # Draw line segment with thickness
                    start, end, thickness = obj
                    self._drawer.drawline(
                        surface, start, end, color, thickness=thickness)
        except Exception as e:
            raise RuntimeError(
                f'Failed to render line segments: {e}')
                

