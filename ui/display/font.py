from abc import ABC, abstractmethod

from ..utility import Color
from .surface import Surface

class Font(ABC):
    """
    Abstract base class for font rendering in the UI system.

    Provides standardized interface for:
    - Text rendering to surfaces
    - System font loading
    - Font metrics
    - Text layout

    Features:
    - Text rendering with color
    - System font integration
    - Size management
    - Error handling
    - Resource management

    Implementation Requirements:
    - Must validate all input parameters
    - Must handle text encoding
    - Must manage font resources
    - Must support color formats
    - Must handle rendering errors

    Resource Management:
    - Font objects should be reusable
    - Font cache should be managed
    - Resources should be released properly
    - Memory usage should be optimized

    Example:
        font = Font.SysFont('Arial', 12)
        surface = font.render('Hello', Color('black'))
    """

    @abstractmethod
    def render(self, text: str, color: Color) -> Surface:
        """Render text to a surface with specified color.

        Creates a new surface containing the rendered text. The surface
        dimensions are automatically calculated to fit the text.

        Args:
            text: String to render (must be non-empty)
            color: Text color (supports named colors, RGB tuples, or Color objects)

        Returns:
            Surface: New surface containing the rendered text

        Raises:
            TypeError: If text is not a string or color has invalid type
            ValueError: If text is empty or contains invalid characters
            RuntimeError: If rendering fails

        Implementation Guidelines:
        1. Validate text is non-empty string
        2. Validate color format
        3. Calculate required surface size
        4. Create appropriately sized surface
        5. Render text with proper alignment
        6. Handle text encoding (UTF-8)
        7. Optimize surface size
        8. Cache rendered results when appropriate
        """
        pass

    @staticmethod
    @abstractmethod
    def SysFont(name: str, fontsize: int) -> 'Font':
        """Create a Font instance from a system font.

        Loads and initializes a font from the system's font directory.
        Handles font substitution if requested font is unavailable.

        Args:
            name: Font family name (e.g., 'Arial', 'Times New Roman')
            fontsize: Font size in points (must be positive)

        Returns:
            Font: New font instance ready for rendering

        Raises:
            TypeError: If parameters have invalid types
            ValueError: If fontsize is not positive
            RuntimeError: If font loading fails

        Implementation Guidelines:
        1. Validate font name is non-empty string
        2. Validate fontsize is positive integer
        3. Search system fonts
        4. Handle font substitution
        5. Initialize font renderer
        6. Cache font instance
        7. Implement fallback strategy
        8. Handle loading errors

        Note:
            Font substitution should prefer visually similar fonts
            when exact match is unavailable.
        """
        pass

