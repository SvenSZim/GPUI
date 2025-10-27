from abc import ABC, abstractmethod


class Surface(ABC):
    """
    Abstract base class for drawable UI surfaces.

    Provides a standardized interface for:
    - Surface size queries
    - Surface composition (blitting)
    - Position validation
    - Boundary checking

    Features:
    - Size management
    - Surface composition
    - Coordinate validation
    - Boundary clipping
    - Error handling

    Implementation Requirements:
    - Must maintain valid dimensions
    - Must handle surface boundaries
    - Must validate input parameters
    - Must handle composition errors
    - Must preserve surface state on errors

    Example:
        class MySurface(Surface):
            def getSize(self) -> tuple[int, int]:
                return self.width, self.height

            def blit(self, surface: Surface, position: tuple[int, int]) -> None:
                # Validate inputs
                # Handle clipping
                # Perform composition
    """

    def _validate_position(self, position: tuple[int, int], operation: str="operation") -> None:
        """Validate a position tuple for surface operations.

        Args:
            position: (x,y) coordinate tuple
            operation: Name of operation for error messages

        Raises:
            TypeError: If position is not a tuple of two integers
            ValueError: If coordinates are negative
        """
        if not isinstance(position, tuple) or len(position) != 2:
            raise TypeError(
                f'Position for {operation} must be a tuple of 2 values, '
                f'got {type(position)}')
        if not all(isinstance(v, int) for v in position):
            raise TypeError(
                f'Position coordinates for {operation} must be integers, '
                f'got {position}')
        if any(v < 0 for v in position):
            raise ValueError(
                f'Position coordinates for {operation} cannot be negative, '
                f'got {position}')

    def _validate_surface(self, surface: 'Surface', operation: str="operation") -> None:
        """Validate a surface for composition operations.

        Args:
            surface: Surface to validate
            operation: Name of operation for error messages

        Raises:
            TypeError: If surface is not a Surface instance
            ValueError: If surface has invalid dimensions
        """
        if not isinstance(surface, Surface):
            raise TypeError(
                f'Surface for {operation} must be a Surface instance, '
                f'got {type(surface)}')
        
        size = surface.getSize()
        if not all(isinstance(v, int) for v in size):
            raise ValueError(
                f'Surface dimensions must be integers, '
                f'got {size}')
        if any(v < 0 for v in size):
            raise ValueError(
                f'Surface dimensions cannot be negative, '
                f'got {size}')

    @abstractmethod
    def getSize(self) -> tuple[int, int]:
        """Get the current dimensions of the surface.

        Returns:
            tuple[int, int]: (width, height) in pixels

        Implementation Guidelines:
        1. Always return positive integers
        2. Cache size if unchanging
        3. Update cache if surface is resizable
        4. Handle dimension changes thread-safely
        """
        pass

    @abstractmethod
    def blit(self, surface: 'Surface', position: tuple[int, int]) -> None:
        """Composite another surface onto this one.

        Performs a pixel-perfect composition of the source surface onto
        this surface at the specified position. Handles:
        - Source surface validation
        - Position validation
        - Boundary clipping
        - Alpha composition
        - Thread safety

        Args:
            surface: Source surface to composite
            position: (x,y) target position for top-left corner

        Raises:
            TypeError: If parameters have invalid types
            ValueError: If position is invalid or surfaces are incompatible
            RuntimeError: If composition fails

        Implementation Guidelines:
        1. Validate source surface and position
        2. Check surface compatibility
        3. Calculate clipping region
        4. Handle alpha composition
        5. Preserve target surface on errors
        6. Ensure thread-safe operation
        """
        pass

