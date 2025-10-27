import os, json
from typing import Any, Union

class tColor:
    """
    A utility class for color management and conversion in the UI system.

    Provides functionality for:
    - RGB color representation
    - Named color lookup (from colors.json)
    - Color format validation
    - Color string parsing
    - Type safety checks

    Colors can be specified as:
    - RGB tuples (0-255 for each channel)
    - Named colors (e.g., 'red', 'blue')
    - Hex color strings

    Example:
        >>> color = tColor((255, 0, 0))  # RGB red
        >>> color = tColor('red')        # Named color
        >>> rgb = color.value            # Get RGB tuple

    Note:
        Named colors are loaded from colors.json file in the same directory.
        Color names are case-sensitive.
    """
    colornames: dict[str, str]={}

    @staticmethod
    def convert_strhex_to_rgb(x: str) -> tuple[int, int, int, int]:
        """Convert a hex color string to an RGBA tuple.

        Supports 6-character (RRGGBB) and 8-character (RRGGBBAA) hex strings.

        Args:
            x: Hex color string (e.g., '#FF0000' or 'FF0000FF')

        Returns:
            tuple[int, int, int, int]: RGBA color values (0-255)

        Raises:
            ValueError: If string is not a valid hex color
        """
        if not isinstance(x, str):
            raise TypeError(f'Hex color must be a string, got {type(x)}')

        # Remove optional '#' prefix and whitespace
        x = x.strip().lstrip('#')

        if len(x) not in (6, 8) or not all(c in '0123456789ABCDEFabcdef' for c in x):
            raise ValueError(f'Invalid hex color format: {x}')

        try:
            x_hex: int = int(x, 16)
            if len(x) == 6:
                r = (x_hex & 0xff0000) >> 16
                g = (x_hex & 0x00ff00) >> 8
                b = (x_hex & 0x0000ff)
                a = 255
            else:
                # 8 chars: RRGGBBAA
                r = (x_hex & 0xff000000) >> 24
                g = (x_hex & 0x00ff0000) >> 16
                b = (x_hex & 0x0000ff00) >> 8
                a = (x_hex & 0x000000ff)
            return (r, g, b, a)
        except ValueError as e:
            raise ValueError(f'Invalid hex color value: {x}') from e

    @staticmethod
    def is_valid_colorname(x: str) -> bool:
        """Check if a color name exists in the color dictionary.

        Args:
            x: Color name to check

        Returns:
            bool: True if color name exists

        Raises:
            TypeError: If x is not a string
        """
        if not isinstance(x, str):
            raise TypeError(f'Color name must be a string, got {type(x)}')
        return x in tColor.colornames
    
    @staticmethod
    def is_valid_color(x: Any) -> bool:
        """Validate a color specification.

        Accepts:
        - Named color strings present in colornames
        - Hex strings ('#RRGGBB' or 'RRGGBBAA')
        - Tuple of 3 (RGB) or 4 (RGBA) integers 0-255
        - tColor instances
        """
        # tColor instance
        if isinstance(x, tColor):
            return True

        # Strings: name, hex, or tuple-like
        if isinstance(x, str):
            s = x.strip()
            # Named color
            if tColor.is_valid_colorname(s):
                return True
            # Hex formats
            try:
                # len 6 or 8 after removing '#'
                sx = s.lstrip('#')
                if len(sx) in (6, 8) and all(c in '0123456789ABCDEFabcdef' for c in sx):
                    return True
            except Exception:
                pass
            # Tuple-like: (r,g,b) or (r,g,b,a)
            if s.startswith('(') and s.endswith(')'):
                parts = [p.strip() for p in s[1:-1].split(',')]
                if len(parts) in (3, 4):
                    try:
                        nums = [int(p) for p in parts]
                        return all(0 <= v <= 255 for v in nums)
                    except ValueError:
                        return False
            return False

        # Tuple input
        if isinstance(x, tuple):
            if len(x) not in (3, 4):
                return False
            if not all(isinstance(v, int) for v in x):
                return False
            if not all(0 <= v <= 255 for v in x):
                return False
            return True

        return False

    # Internal representation is RGBA tuple (r,g,b,a)
    value: tuple[int, int, int, int]  # rgba color value

    def __init__(self, value: tuple[int, int, int] | tuple[int, int, int, int] | str) -> None:
        """Initialize a new Color instance.

        Creates a color from either an RGB tuple or a named color string.

        Args:
            value: Either an RGB tuple (r,g,b) with values 0-255
                  or a named color string (e.g., 'red')

        Raises:
            TypeError: If value has invalid type
            ValueError: If RGB values are out of range or color name is invalid
        """
        if isinstance(value, str):
            # Named color lookup
            if tColor.is_valid_colorname(value):
                self.value = tColor.convert_strhex_to_rgb(tColor.colornames[value])
            else:
                # Try hex or tuple-like string
                s = value.strip()
                # Hex
                try:
                    if s.startswith('#') or len(s.lstrip('#')) in (6, 8):
                        self.value = tColor.convert_strhex_to_rgb(s)
                    elif s.startswith('(') and s.endswith(')'):
                        parts = [p.strip() for p in s[1:-1].split(',')]
                        nums = [int(p) for p in parts]
                        if len(nums) == 3:
                            r, g, b = nums
                            a = 255
                        elif len(nums) == 4:
                            r, g, b, a = nums
                        else:
                            raise ValueError
                        if not all(0 <= v <= 255 for v in (r, g, b, a)):
                            raise ValueError
                        self.value = (r, g, b, a)
                    else:
                        raise ValueError
                except ValueError:
                    raise ValueError(
                        f'Invalid color string: {value}\n'
                        f'Available colors: {sorted(tColor.colornames.keys())}')
        elif isinstance(value, tuple):
            if len(value) == 3:
                if not all(isinstance(v, int) for v in value):
                    raise TypeError('RGB values must be integers')
                if not all(0 <= v <= 255 for v in value):
                    raise ValueError('RGB values must be between 0 and 255')
                r, g, b = value
                a = 255
                self.value = (r, g, b, a)
            elif len(value) == 4:
                if not all(isinstance(v, int) for v in value):
                    raise TypeError('RGBA values must be integers')
                if not all(0 <= v <= 255 for v in value):
                    raise ValueError('RGBA values must be between 0 and 255')
                self.value = value
            else:
                raise ValueError(f'Color tuple must have 3 or 4 values, got {len(value)}')
        else:
            raise TypeError(
                f'Color value must be RGB tuple or color name string, '
                f'got {type(value)}')

    def __eq__(self, other: object) -> bool:
        """Compare two colors for equality.

        Args:
            other: Another color to compare with

        Returns:
            bool: True if colors have same RGB values
        """
        if not isinstance(other, tColor):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        """Get string representation of the color.

        Returns:
            str: Color in rgb(r,g,b) format
        """
        return f'rgb{self.value}'

    def to_hex(self, include_alpha: bool = False) -> str:
        """Convert color to hex string.

        Args:
            include_alpha: If True include alpha channel (8 chars)

        Returns:
            Hex string without leading '#'
        """
        r, g, b, a = self.value
        if include_alpha:
            return ('%02x%02x%02x%02x' % (r, g, b, a)).upper()
        return ('%02x%02x%02x' % (r, g, b)).upper()

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Get RGB values as a tuple.

        Returns:
            tuple[int, int, int]: (r,g,b) values 0-255
        """
        r, g, b, _ = self.value
        return (r, g, b)

    @property
    def normalized_rgb(self) -> tuple[float, float, float]:
        """Get normalized RGB values as floats 0.0-1.0.

        Returns:
            tuple[float, float, float]: (r,g,b) values 0.0-1.0
        """
        r, g, b, _ = self.value
        return (r / 255.0, g / 255.0, b / 255.0)

    @property
    def normalized_rgba(self) -> tuple[float, float, float, float]:
        """Get normalized RGBA values as floats 0.0-1.0.

        Returns:
            tuple[float, float, float, float]: (r,g,b,a) values 0.0-1.0
        """
        r, g, b, a = self.value
        return (r / 255.0, g / 255.0, b / 255.0, a / 255.0)

    def with_alpha(self, alpha: int) -> tuple[int, int, int, int]:
        """Create RGBA tuple with this color and given alpha.

        Args:
            alpha: Alpha value 0-255

        Returns:
            tuple[int, int, int, int]: (r,g,b,a) values

        Raises:
            ValueError: If alpha is out of range
        """
        if not isinstance(alpha, int):
            raise TypeError('Alpha value must be an integer')
        if not 0 <= alpha <= 255:
            raise ValueError('Alpha value must be between 0 and 255')
        r, g, b, _ = self.value
        return (r, g, b, alpha)

    def with_alpha_color(self, alpha: int) -> 'tColor':
        """Return a new tColor with the provided alpha value."""
        r, g, b, _ = self.value
        return tColor((r, g, b, alpha))

    def blend(self, other: 'tColor', factor: float) -> 'tColor':
        """Blend this color with another using given factor.

        Args:
            other: Color to blend with
            factor: Blend factor 0.0-1.0 (0=this color, 1=other color)

        Returns:
            tColor: New blended color

        Raises:
            TypeError: If inputs have invalid types
            ValueError: If factor is out of range
        """
        if not isinstance(other, tColor):
            raise TypeError(f'other must be a tColor, got {type(other)}')
        if not isinstance(factor, (int, float)):
            raise TypeError(f'factor must be a number, got {type(factor)}')
        if not 0 <= factor <= 1:
            raise ValueError('factor must be between 0 and 1')

        inv_factor = 1.0 - factor
        r = int(self.value[0] * inv_factor + other.value[0] * factor)
        g = int(self.value[1] * inv_factor + other.value[1] * factor)
        b = int(self.value[2] * inv_factor + other.value[2] * factor)
        a = int(self.value[3] * inv_factor + other.value[3] * factor)
        return tColor((r, g, b, a))

filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colors.json')
with open(filepath, 'r') as file:
    tColor.colornames = json.load(file)


def get_nearest_color_name(rgb: tuple[int, int, int] | tuple[int, int, int, int]) -> str:
    """Find the named color closest to given RGB(A) values.

    Uses simple Euclidean distance in RGB space to find the nearest color.

    Args:
        rgb: RGB or RGBA tuple to match

    Returns:
        str: Name of the closest matching color

    Raises:
        TypeError: If rgb is not a valid tuple
        ValueError: If rgb values are out of range
    """
    if not isinstance(rgb, tuple) or len(rgb) not in (3, 4):
        raise TypeError('rgb must be a tuple of 3 or 4 values')
    if not all(isinstance(v, int) for v in rgb):
        raise TypeError('rgb values must be integers')
    if not all(0 <= v <= 255 for v in rgb):
        raise ValueError('rgb values must be between 0 and 255')

    # Compare only RGB components
    target = rgb[:3]

    def color_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
        return sum((v1 - v2) ** 2 for v1, v2 in zip(c1, c2)) ** 0.5

    min_dist = float('inf')
    nearest_name = None

    for name, hex_value in tColor.colornames.items():
        color_rgba = tColor.convert_strhex_to_rgb(hex_value)
        color_rgb = color_rgba[:3]
        dist = color_distance(target, color_rgb)
        if dist < min_dist:
            min_dist = dist
            nearest_name = name

    return nearest_name if nearest_name else 'black'


# Type alias for color values accepted by the UI system
# Can be:
# - Named color string (e.g., 'red')
# - RGB or RGBA tuple (e.g., (255, 0, 0) or (255,0,0,128))
# - tColor instance
Color = Union[str, tuple[int, int, int], tuple[int, int, int, int], tColor]
