from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum
from typing import Any, Optional, override

from .....utility import tColor, Color
from ..atomdata import AtomData


bool4 = tuple[bool, bool, bool, bool]

class AltMode(Enum):
    DEFAULT         = 0x00
    STRIPED_V       = 0x01
    STRIPED_H       = 0x02
    CHECKERBOARD    = 0x03

class Filters(Enum):
    DEFAULT         = 0x00
    LINEAR          = 0x01
    QUADRATIC       = 0x03

@dataclass
class BoxData(AtomData):
    """
    BoxData is a configuration class for Box atom rendering properties.

    This class stores and manages the following properties:
    - colors: Color definitions for each partition/section
    - partialInset: Inset/padding values for sections
    - partitioning: Grid layout configuration (columns, rows, labels)
    - altMode: Pattern fill mode for each section (checkerboard, stripes)
    - orders: Order of colors for pattern fills
    - altLen: Size parameters for pattern fills
    - filters: Geometric filters for special rendering effects

    All properties are dictionary-based to support both global ('') and
    partition-specific settings.
    """
    colors      : dict[str, Optional[Color]]    = field(default_factory=lambda:{'': None})
    partialInset: dict[str, tuple[float, float] | float | tuple[int, int] | int] = field(default_factory=lambda:{'': 0})
    partitioning: tuple[int, int, list[str]]    = field(default_factory=lambda:(1, 1, ['']))
    altMode     : dict[str, AltMode]            = field(default_factory=lambda:{'': AltMode.DEFAULT})
    orders      : dict[str, list[str]]          = field(default_factory=lambda:{'': ['']})
    altLen      : dict[str, float | int]        = field(default_factory=lambda:{'': 10})
    filters     : dict[str, Filters | tuple[Filters, tuple[float, float, tuple[float, float]], bool]] = field(default_factory=lambda:{'': Filters.DEFAULT})

    @override
    def copy(self) -> 'BoxData':
        return BoxData(deepcopy(self.colors), deepcopy(self.partialInset),
                       deepcopy(self.partitioning), deepcopy(self.altMode),
                       deepcopy(self.orders), deepcopy(self.altLen),
                       deepcopy(self.filters))

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'BoxData':
        """Create a BoxData instance from a dictionary of arguments.

        Args:
            args (dict[str, Any]): Configuration arguments for box properties.
                Supports keys: boxcolor/colors, boxinset/inset, boxpart/partitioning,
                boxmode/fillmode, boxsize/fillsize, boxfilter/filter

        Returns:
            BoxData: A new BoxData instance configured with the provided arguments.
        """
        if not isinstance(args, dict):
            raise TypeError(f'args must be a dict, got {type(args)}')

        data: BoxData = BoxData()
        data.set(args, False)
        return data

    # -------------------- access-point --------------------

    def _validateLabel(self, label: str) -> None:
        """Validate a partition label.

        Args:
            label (str): The label to validate

        Raises:
            TypeError: If label is not a string
            ValueError: If label is invalid
        """
        if not isinstance(label, str):
            raise TypeError(f'Label must be a string, got {type(label)}')
        if len(label) > 100:  # Reasonable max length to prevent abuse
            raise ValueError(f'Label too long (max 100 chars): {label}')

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        """Configure BoxData properties from a dictionary of arguments.

        This method parses and validates various box configuration options including:
        - colors: Box fill colors (global or per partition)
        - insets: Box padding/margins
        - partitioning: Grid layout settings
        - fill modes: Pattern fill types
        - fill sizes: Pattern size parameters
        - filters: Geometric render filters

        Args:
            args (dict[str, Any]): Configuration dictionary
            skips (bool): If True, only validates arguments without applying them

        Returns:
            bool: True if any properties were modified or would be modified

        Raises:
            TypeError: If args is not a dictionary
            ValueError: If argument values are invalid
        """
        if not isinstance(args, dict):
            raise TypeError(f'args must be a dict, got {type(args)}')
        if not isinstance(skips, bool):
            raise TypeError(f'skips must be a bool, got {type(skips)}')

        s: bool = False
        for arg, v in args.items():
            if arg not in ['boxpart', 'partitioning', 'part']:
                if not isinstance(v, str):
                    continue
                values = v.split(';')
                labelValuePairs: list[list[str]] = [vv.split(':') for vv in values]
                for vv in labelValuePairs:
                    label: str
                    value: str
                    if len(vv) == 1:
                        label = ''
                        value = vv[0]
                    else:
                        label = BoxData.parseLabel(vv[0])
                        value = vv[1]
                    match arg:
                        case 'boxinset' | 'inset' | 'partial' | 'shrink':
                            s = True
                            if not skips:
                                self.partialInset[label] = BoxData.parsePartial(value)
                        case 'boxcolor' | 'colors' | 'color' | 'col':
                            s = True
                            if not skips:
                                self.colors[label] = tColor(value)
                        case 'boxorder' | 'sectionorders' | 'orders' | 'ord':
                            s = True
                            if not skips:
                                self.orders[label] = BoxData.parseList(value)
                        case 'boxmode' | 'fillmodes' | 'fillmode' | 'fills' | 'fill' | 'altmodes' | 'altmode' | 'modes' | 'mode':
                            s = True
                            if not skips:
                                match value:
                                    case 'checkerboard' | 'cb':
                                        self.altMode[label] = AltMode.CHECKERBOARD
                                    case 'striped_vert' | 'strv':
                                        self.altMode[label] = AltMode.STRIPED_V
                                    case 'striped_hor' | 'strh':
                                        self.altMode[label] = AltMode.STRIPED_H
                        case 'boxsize' | 'fillsizes' | 'fillsize' | 'innersizings' | 'innersizing' | 'sizes' | 'size':
                            s = True
                            if not skips:
                                match value:
                                    case 's':
                                        self.altLen[label] = 10
                                    case 'l':
                                        self.altLen[label] = 20
                                    case _:
                                        self.altLen[label] = BoxData.parseNum(value)
                        case 'boxfilter' | 'filters' | 'filter' | 'filt':
                            s = True
                            if not skips:
                                filtype, *options = [vvv.strip() for vvv in value.split('=')]
                                if len(options) == 0:
                                    continue
                                inv: bool = False
                                if filtype[0] == 'i':
                                    inv = True
                                    filtype = filtype[1:]
                                match filtype[0].lower():
                                    case 'l' | 't':
                                        #linear/triangle filter
                                        self.filters[label] = (Filters.LINEAR, BoxData.parseFilterArgs(options[0]), inv)
                                    case 'q' | 'c':
                                        #quadratic/circle filter
                                        self.filters[label] = (Filters.QUADRATIC, BoxData.parseFilterArgs(options[0]), inv)
                                    case _:
                                        pass
            else:
                match arg:
                    case 'boxpart' | 'partitioning' | 'part':
                        s = True
                        if not skips:
                            self.partitioning = BoxData.parsePartition(v)

        return s

    @staticmethod
    def _validatePartitioning(cols: int, rows: int, labels: list[str]) -> None:
        """Validate partitioning parameters.

        Args:
            cols (int): Number of columns
            rows (int): Number of rows
            labels (list[str]): Partition labels

        Raises:
            TypeError: If parameters have invalid types
            ValueError: If parameters have invalid values
        """
        if not isinstance(cols, int) or not isinstance(rows, int):
            raise TypeError('Columns and rows must be integers')
        if cols < 1 or rows < 1:
            raise ValueError('Columns and rows must be positive')
        if not isinstance(labels, list):
            raise TypeError('Labels must be a list')
        if len(labels) != cols * rows:
            raise ValueError(f'Expected {cols * rows} labels, got {len(labels)}')
        if not all(isinstance(label, str) for label in labels):
            raise TypeError('All labels must be strings')

    @staticmethod
    def _validateAltMode(mode: Any) -> AltMode:
        """Validate and convert alt mode value.

        Args:
            mode: The mode value to validate

        Returns:
            AltMode: Valid alt mode enum value

        Raises:
            TypeError: If mode is not an AltMode enum
            ValueError: If mode value is invalid
        """
        if not isinstance(mode, AltMode):
            raise TypeError(f'Mode must be an AltMode enum, got {type(mode)}')
        return mode

    @staticmethod
    def _validateFilter(filt: Any) -> 'Filters | tuple[Filters, tuple[float, float, tuple[float, float]], bool]':
        """Validate filter configuration.

        Args:
            filt: The filter configuration to validate

        Returns:
            Valid filter configuration

        Raises:
            TypeError: If filter has invalid type
            ValueError: If filter parameters are invalid
        """
        if isinstance(filt, Filters):
            return filt
        if not isinstance(filt, tuple) or len(filt) != 3:
            raise TypeError('Complex filter must be a tuple of (Filters, params, bool)')
        if not isinstance(filt[0], Filters):
            raise TypeError('First filter tuple element must be a Filters enum')
        if not isinstance(filt[2], bool):
            raise TypeError('Third filter tuple element must be a bool')
        return filt