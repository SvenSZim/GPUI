from abc import ABC, abstractmethod

from ..utility import Color, Rect
from .surface import Surface

class SurfaceDrawer(ABC):
    """
    Abstract base class defining the drawing interface for UI surfaces.

    The SurfaceDrawer provides a standard interface for rendering operations:
    - Line drawing with thickness control
    - Rectangle drawing (filled and outlined)
    - Surface composition
    
    Features:
    - Coordinate validation
    - Color type checking
    - Thickness validation
    - Fill mode control
    - Error handling for invalid inputs

    Implementation Requirements:
    - Must validate all input parameters
    - Must handle surface boundaries
    - Must support color formats from Color type
    - Must preserve surface state on errors

    Example Implementation:
        class MyDrawer(SurfaceDrawer):
            @staticmethod
            def drawline(surface, start, end, color, thickness=1):
                # Validate inputs
                # Convert color to implementation format
                # Draw line with validated parameters
    """

    @staticmethod
    @abstractmethod
    def drawline(surface: Surface, startpoint: tuple[int, int], endpoint: tuple[int, int], color: Color, thickness: int=1) -> None:
        """
        Draw a line between two points on a surface.

        Renders an anti-aliased line of specified thickness between start and end points.
        Handles line clipping at surface boundaries.

        Args:
            surface: Target surface for drawing
            startpoint: (x,y) coordinates of line start
            endpoint: (x,y) coordinates of line end
            color: Line color (supports named colors, RGB tuples, or Color objects)
            thickness: Line thickness in pixels (default=1)

        Raises:
            TypeError: If parameters have invalid types
            ValueError: If coordinates are invalid or thickness is less than 1
            RuntimeError: If drawing operation fails

        Implementation Guidelines:
        1. Validate surface is not None and is a Surface instance
        2. Validate points are valid integer tuples
        3. Validate color is a supported format
        4. Validate thickness is positive integer
        5. Clip line to surface boundaries
        6. Handle drawing errors gracefully
        """
        pass

    @staticmethod
    @abstractmethod
    def drawrect(surface: Surface, rect: Rect, color: Color, fill: bool=True) -> None:
        """
        Draw a rectangle on a surface.

        Renders a rectangle that can be either filled or outlined. Handles:
        - Rectangle clipping at surface boundaries
        - Zero-size rectangles (no operation)
        - Negative dimensions (normalized automatically)

        Args:
            surface: Target surface for drawing
            rect: Rectangle defining position and size
            color: Fill or outline color (supports named colors, RGB tuples, or Color objects)
            fill: If True, fills rectangle with solid color;
                 if False, draws only the outline (default=True)

        Raises:
            TypeError: If parameters have invalid types
            ValueError: If rectangle has invalid dimensions
            RuntimeError: If drawing operation fails

        Implementation Guidelines:
        1. Validate surface is not None and is a Surface instance
        2. Validate rect is a valid Rect instance
        3. Validate color is a supported format
        4. Normalize rectangle (handle negative dimensions)
        5. Clip rectangle to surface boundaries
        6. Handle zero-size cases
        7. Apply fill mode appropriately
        8. Handle drawing errors gracefully
        """
        pass
