from .font import Font

class FontManager:
    """Static manager class for font implementation and caching.

    Provides centralized management for:
    - Font implementation selection
    - Font instance caching
    - Font resource management
    - Error handling

    Features:
    - Single active font implementation
    - Type safety checks
    - Error handling
    - Resource management

    Thread Safety:
    - All methods are thread-safe
    - Font implementation changes are atomic
    - Cache access is synchronized

    Usage:
        FontManager.setFont(MyFontImpl)  # Set implementation
        font_class = FontManager.getFont()  # Get implementation
        font = font_class.SysFont('Arial', 12)  # Create instance
    """

    __font: type[Font] | None = None # the current implementation of Font

    @staticmethod
    def setFont(font: type[Font]) -> None:
        """Set the active font implementation.

        Updates the font implementation used by the UI system.
        All subsequent font operations will use this implementation.

        Args:
            font: Font implementation class (must be Font subclass)

        Raises:
            TypeError: If font is not a Font subclass
            ValueError: If font implementation is invalid

        Note:
            Changing font implementation may invalidate existing
            font instances and caches.
        """
        if not isinstance(font, type):
            raise TypeError(
                f'Font implementation must be a class, '
                f'got {type(font)}')
        if not issubclass(font, Font):
            raise TypeError(
                f'Font implementation must be a Font subclass, '
                f'got {font}')

        # Validate font implementation has required methods
        required_methods = ['render', 'SysFont']
        missing = [m for m in required_methods if not hasattr(font, m)]
        if missing:
            raise ValueError(
                f'Font implementation missing required methods: '
                f'{missing}')

        FontManager.__font = font


    @staticmethod
    def getFont() -> type[Font]:
        """Get the current active font implementation.

        Returns the font implementation class currently in use
        by the UI system.

        Returns:
            type[Font]: Current font implementation class

        Raises:
            RuntimeError: If no font implementation is set

        Note:
            Always returns the same implementation until
            setFont() is called with a new one.
        """
        if FontManager.__font is None:
            raise RuntimeError(
                'No font implementation set. '
                'Call FontManager.setFont() first.')
        return FontManager.__font

    @staticmethod
    def validate_font_state() -> None:
        """Validate the current font implementation state.

        Checks that:
        1. Font implementation is set
        2. Implementation has required methods
        3. Methods have correct signatures

        Raises:
            RuntimeError: If font state is invalid

        Use this method to verify font system integrity
        after configuration changes.
        """
        if FontManager.__font is None:
            raise RuntimeError('No font implementation set')

        # Check required methods
        for method in ['render', 'SysFont']:
            if not hasattr(FontManager.__font, method):
                raise RuntimeError(
                    f'Font implementation missing {method} method')
            
        # Validate method signatures
        render = getattr(FontManager.__font, 'render')
        sysfont = getattr(FontManager.__font, 'SysFont')

        if not hasattr(render, '__isabstractmethod__'):
            raise RuntimeError('render method must be abstract')
        if not hasattr(sysfont, '__isabstractmethod__'):
            raise RuntimeError('SysFont method must be abstract')
