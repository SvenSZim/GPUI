from abc import ABC, abstractmethod
from typing import Any, Optional

class Parsable(ABC):
    """Abstract base class providing parsing utilities for UI elements.

    This class provides a collection of static methods for parsing various
    data types and formats commonly used in UI element definitions.

    Features:
    - Binary string parsing
    - Numeric extraction and parsing
    - List parsing with separator customization
    - Color parsing and validation
    - Label validation
    - Argument validation

    Thread Safety:
    - All methods are stateless and thread-safe
    - No shared mutable state
    
    Version Info:
    - Supports XML format v1.0
    - Compatible with style sheets v1.0
    """

    VERSION = "1.0.0"  # Current version of the parsing implementation
    XML_VERSION = "1.0"  # Supported XML format version
    STYLE_VERSION = "1.0"  # Supported style sheet version
    
    @staticmethod
    def parseBinary(s: str) -> int:
        """Parse a binary string to integer.

        Extracts valid binary digits (0,1) and converts to integer.

        Args:
            s: String containing binary digits

        Returns:
            Integer value of binary string, or 0 if invalid

        Examples:
            >>> Parsable.parseBinary('1010')
            10
            >>> Parsable.parseBinary('invalid')
            0
        """
        if not isinstance(s, str):
            return 0

        nn = ''
        for c in s:
            if c in {'0', '1'}:
                nn += c

        try:
            return int(nn, 2) if nn else 0
        except ValueError:
            return 0

    @staticmethod
    def extractNum(s: str) -> str:
        """Extract numeric characters from a string.

        Filters out all non-numeric characters and returns
        the concatenated digits.

        Args:
            s: Input string to extract numbers from

        Returns:
            String of consecutive digits, or '0' if none found

        Examples:
            >>> Parsable.extractNum('abc123def')
            '123'
            >>> Parsable.extractNum('no-numbers')
            '0'
        """
        if not isinstance(s, str):
            return '0'

        # Extract all numeric characters
        nn = ''.join(c for c in s if c.isdigit())
        return nn if nn else '0'

    @staticmethod
    def parseNum(s: str) -> int | float:
        """Parse a string into a number (integer or float).

        Handles both integer and decimal numbers. For decimals,
        maintains proper decimal place value.

        Args:
            s: String to parse as number

        Returns:
            int: For integer strings
            float: For decimal strings

        Examples:
            >>> Parsable.parseNum('123')
            123
            >>> Parsable.parseNum('12.34')
            12.34
            >>> Parsable.parseNum('abc12.34xyz')
            12.34
        """
        if not isinstance(s, str):
            return 0

        s = s.strip()

        try:
            if '.' in s:
                # Handle decimal numbers
                whole, frac = s.split('.', 1)  # Split on first period only
                vk = Parsable.extractNum(whole)
                nk = Parsable.extractNum(frac)
                # Convert to proper decimal value
                return int(vk) + int(nk)/(10**len(nk)) if nk else int(vk)
            else:
                # Handle integers
                return int(Parsable.extractNum(s))
        except (ValueError, ZeroDivisionError):
            return 0

    @staticmethod
    def parseList(s: str, separator: str=',') -> list[str]:
        """Parse a string into a list using specified separator.

        Handles optional square bracket notation and trims whitespace.

        Args:
            s: String to parse into list
            separator: Character to split on (default ',')

        Returns:
            List of trimmed string elements

        Examples:
            >>> Parsable.parseList('[a, b, c]')
            ['a', 'b', 'c']
            >>> Parsable.parseList('x|y|z', '|')
            ['x', 'y', 'z']
        """
        if not isinstance(s, str):
            return []
        if not isinstance(separator, str) or not separator:
            separator = ','

        ret: list[str] = []
        s = s.strip()
        if not s:
            return ret

        # Handle bracketed lists [a,b,c]
        content = s
        if s.startswith('[') and s.endswith(']'):
            content = s[1:-1]

        # Split and clean elements
        return [elem.strip() for elem in content.split(separator) if elem.strip()]

    @staticmethod
    def parseFilterArgs(s: str) -> tuple[float, float, tuple[float, float]]:
        """Parse filter arguments from a string specification.

        Parses strings in formats:
        - "(x)" -> (x, 0, (0,0))
        - "(x,y)" -> (x, y, (0,0))
        - "(x,y,z)" -> (x, y, (z,0))
        - "(x,y,z+w)" -> (x, y, (z,w))

        Args:
            s: Filter argument string

        Returns:
            Tuple of (x, y, (z,w)) where:
            - x,y: Primary filter values
            - z,w: Secondary filter values

        Examples:
            >>> Parsable.parseFilterArgs('(1.5)')
            (1.5, 0.0, (0.0, 0.0))
            >>> Parsable.parseFilterArgs('(1,2,3+4)')
            (1.0, 2.0, (3.0, 4.0))
        """
        if not isinstance(s, str):
            return (0.0, 0.0, (0.0, 0.0))

        # Strip and validate
        s = s.strip()
        if not s:
            return (0.0, 0.0, (0.0, 0.0))

        # Extract content between parentheses
        content = s
        if '(' in s and ')' in s:
            try:
                start = s.index('(') + 1
                end = s.rindex(')')
                if end > start:
                    content = s[start:end]
            except ValueError:
                return (0.0, 0.0, (0.0, 0.0))

        # Parse components
        try:
            parts = [v.strip() for v in Parsable.parseList(content)]
            match len(parts):
                case 1:
                    return (Parsable.parseNum(parts[0]), 0.0, (0.0, 0.0))
                case 2:
                    return (Parsable.parseNum(parts[0]), Parsable.parseNum(parts[1]), (0.0, 0.0))
                case _:
                    if '+' in parts[2]:
                        u, v = [Parsable.parseNum(m) for m in parts[2].split('+')][:2]
                        return (Parsable.parseNum(parts[0]), Parsable.parseNum(parts[1]), (u, v))
                    elif parts[2][-1] == 'y':
                        return (Parsable.parseNum(parts[0]), Parsable.parseNum(parts[1]), (0.0, Parsable.parseNum(parts[2])))
                    else:
                        return (Parsable.parseNum(parts[0]), Parsable.parseNum(parts[1]), (Parsable.parseNum(parts[2]), 0.0))
        except (ValueError, IndexError):
            return (0.0, 0.0, (0.0, 0.0))

    @staticmethod
    def parseLabel(s: str) -> str:
        """Parse and validate a label string.

        Valid labels:
        - Must not start with a number
        - Must not contain special characters
        - Are case-sensitive
        - May contain letters, numbers (not first), underscores

        Args:
            s: Label string to validate

        Returns:
            Validated label string

        Raises:
            ValueError: If label format is invalid

        Examples:
            >>> Parsable.parseLabel('validLabel')  # Valid
            'validLabel'
            >>> Parsable.parseLabel('2invalid')  # Invalid, starts with number
            ValueError
        """
        if not isinstance(s, str):
            raise ValueError('Label must be a string')

        s = s.strip()
        if not s:
            raise ValueError('Label cannot be empty')

        # Check first character
        if s[0].isdigit():
            raise ValueError(
                f'Label {repr(s)} cannot start with a number')

        # Check forbidden characters
        forbidden = {'=', ':', '[', ']', '{', '}', ' ', '\t', '\n'}
        if bad_chars := {c for c in s if c in forbidden}:
            raise ValueError(
                f'Label {repr(s)} contains forbidden characters: {bad_chars}')

        return s

    @staticmethod
    def parsePartial(s: str) -> tuple[float, float] | float | tuple[int, int] | int:
        """Parse a string into a single number or coordinate pair.

        Supports formats:
        1. Single number: "123" -> 123
        2. Coordinate pair: "1,2" -> (1,2)
        Numbers can be integers or floats.

        Args:
            s: String to parse

        Returns:
            - Single number (int or float) for single values
            - Tuple of (x,y) for coordinate pairs

        Examples:
            >>> Parsable.parsePartial('123')
            123
            >>> Parsable.parsePartial('1.5,2.5')
            (1.5, 2.5)
        """
        if not isinstance(s, str):
            return 0

        s = s.strip()
        if not s:
            return 0

        try:
            if ',' in s:
                # Parse coordinate pair
                x, y = list(map(str.strip, s.split(',', 1)))[:2]
                return (Parsable.parseNum(x), Parsable.parseNum(y))
            else:
                # Parse single value
                return Parsable.parseNum(s)
        except (ValueError, IndexError):
            return 0

    @staticmethod
    def handle_parse_error(value: str, expected_type: str, context: str = '') -> None:
        """Raise a formatted parse error.

        Helper to generate consistent parse error messages.

        Args:
            value: The invalid value that failed to parse
            expected_type: Description of expected format
            context: Optional context for error message

        Raises:
            ValueError: With formatted error message

        Example:
            >>> Parsable.handle_parse_error('abc', 'number', 'width')
            ValueError: Invalid width 'abc': expected number
        """
        ctx = f' {context}' if context else ''
        raise ValueError(
            f'Invalid{ctx} {repr(value)}: '
            f'expected {expected_type}')

    @staticmethod
    def adjustList(l: list[str], adjustments: list[str]) -> list[str]:
        """Apply a series of adjustments to a list of strings.

        Supports two types of adjustments:
        1. Direct value: Replace current index with value
        2. Indexed value: "n=value" sets index n-1 to value

        Args:
            l: Base list to modify
            adjustments: List of adjustment strings

        Returns:
            Modified list after applying adjustments

        Examples:
            >>> Parsable.adjustList(['a', 'b', 'c'], ['x', 'y'])
            ['x', 'y', 'c']
            >>> Parsable.adjustList(['a', 'b', 'c'], ['2=x', 'y'])
            ['a', 'x', 'y']
        """
        if not isinstance(l, list) or not all(isinstance(x, str) for x in l):
            raise ValueError('First argument must be list of strings')
        if not isinstance(adjustments, list):
            raise ValueError('Adjustments must be a list')

        result = l.copy()  # Work on a copy to preserve original
        currentIdx = 0

        for adj in adjustments:
            if not isinstance(adj, str):
                continue

            # Handle indexed assignments (n=value)
            if '=' in adj:
                try:
                    pos, value = adj.split('=', 1)
                    jumpTo = int(Parsable.extractNum(pos)) - 1
                    if 0 <= jumpTo < len(result):
                        currentIdx = jumpTo
                    adj = value
                except (ValueError, IndexError):
                    continue

            # Apply adjustment if index is valid
            if 0 <= currentIdx < len(result):
                result[currentIdx] = adj
            currentIdx += 1

        return result


    @staticmethod
    def parsePartition(s: str) -> tuple[int, int, list[str]]:
        """Parse a partition specification string.

        Format: "WxH;[row1][row2]...[rowN]"
        Where:
        - W,H are dimensions (supports x,*,-,/ as separators)
        - [] groups define row contents
        - Row contents can use index=value format

        Args:
            s: Partition specification string

        Returns:
            Tuple of (width, height, cell_contents)

        Examples:
            >>> Parsable.parsePartition('2x2;[a,b][c,d]')
            (2, 2, ['a', 'b', 'c', 'd'])
            >>> Parsable.parsePartition('2x3;[1=x,y]')
            (2, 3, ['', '', 'x', 'y', '', ''])

        Raises:
            ValueError: If partition format is invalid
        """
        if not isinstance(s, str):
            raise TypeError(f'Expected string, got {type(s)}')

        # Default values
        x: int = 1
        y: int = 1

        try:
            # Split into size and content parts
            parts = s.strip().split(';', 1)
            if not parts:
                return (x, y, [''])

            # Parse dimensions
            size = parts[0].strip()
            if size:
                # Try each supported separator
                for sep in ['x', '*', '-', '/']:
                    if sep in size:
                        try:
                            dims = size.split(sep, 1)
                            if len(dims) == 2:
                                # Extract and validate dimensions
                                width = int(dims[0].strip())
                                height = int(dims[1].strip())
                                if width > 0 and height > 0:
                                    x, y = width, height
                                    break
                        except ValueError:
                            continue

            # Initialize result grid
            total_cells = x * y
            cells = [''] * total_cells

            # Parse content if provided
            if len(parts) > 1:
                content = parts[1].strip()
                row = 0

                i = 0
                while i < len(content) and row < y:
                    # Find complete row definition [...]]
                    if content[i] == '[':
                        end = content.find(']', i)
                        if end == -1:
                            break

                        # Extract and parse row content
                        row_content = content[i+1:end]
                        row_cells = Parsable.parseList(row_content)
                        
                        # Apply row values with adjustments
                        start_idx = row * x
                        if start_idx < total_cells:
                            cells[start_idx:start_idx + x] = \
                                Parsable.adjustList(
                                    cells[start_idx:start_idx + x],
                                    row_cells)
                        
                        row += 1
                        i = end + 1
                    else:
                        i += 1

            return (x, y, cells)

        except Exception as e:
            raise ValueError(
                f'Invalid partition format: {s}. '
                f'Expected "WxH;[row1][row2]...[rowN]"') from e

    @staticmethod
    def validateRequiredArgs(args: dict[str, Any], required: list[str], context: str='') -> None:
        """Validate that all required arguments are present.
        
        Args:
            args (dict[str, Any]): Arguments to validate
            required (list[str]): List of required argument names
            context (str): Optional context for error message
            
        Raises:
            ValueError: If any required arguments are missing
        """
        missing = [arg for arg in required if arg not in args]
        if missing:
            ctx = f' for {context}' if context else ''
            raise ValueError(f'Missing required arguments{ctx}: {", ".join(missing)}')

    @staticmethod
    def getMinRequiredChildren() -> int:
        """Get minimum number of child elements required.
        
        Returns:
            int: Minimum number of child elements needed
        """
        return 0

    @staticmethod
    @abstractmethod
    def parseFromArgs(args: dict[str, Any]) -> 'Parsable':
        """Parse instance from argument dictionary.
        
        This method should validate required arguments and parse values into
        an instance of the class.
        
        Args:
            args (dict[str, Any]): Dictionary of arguments to parse
            
        Returns:
            Parsable: New instance initialized from args
            
        Raises:
            ValueError: If required args are missing or values are invalid
        """
        pass

