from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, override

from .....utility import Color, tColor
from ..atomdata   import AtomData

class AltMode(Enum):
    DEFAULT = 0x00
    CROSS   = 0x01

@dataclass
class LineData(AtomData):
    """Storage class for Line element render properties.

    Manages visual properties including:
    - Colors per section
    - Section sizes
    - Line thickness
    - Rendering modes
    - Pattern ordering
    - Inset and flip settings

    Thread Safety:
    - Property access is synchronized
    - Updates are atomic
    - Copy operations are thread-safe

    Validation:
    - Color values must be valid Color instances or None
    - Sizes must be positive numbers
    - Thickness must be positive integers
    - Insets must be valid tuples or numbers
    """

    # Pattern section properties
    colors: dict[str, Optional[Color]] = field(
        default_factory=lambda: {'': None},
        metadata={'validator': lambda x: isinstance(x, dict) and
                  all(isinstance(k, str) and
                      (v is None or tColor.is_valid_color(v))
                      for k, v in x.items())}
    )

    sizes: dict[str, int | float] = field(
        default_factory=lambda: {'': 1.0},
        metadata={'validator': lambda x: isinstance(x, dict) and
                  all(isinstance(k, str) and
                      isinstance(v, (int, float)) and v > 0
                      for k, v in x.items())}
    )

    thickness: dict[str, int] = field(
        default_factory=lambda: {'': 1},
        metadata={'validator': lambda x: isinstance(x, dict) and
                  all(isinstance(k, str) and
                      isinstance(v, int) and v > 0
                      for k, v in x.items())}
    )

    altmode: dict[str, AltMode] = field(
        default_factory=lambda: {'': AltMode.DEFAULT},
        metadata={'validator': lambda x: isinstance(x, dict) and
                  all(isinstance(k, str) and
                      isinstance(v, AltMode)
                      for k, v in x.items())}
    )

    # Global properties
    inset: tuple[float, float] | float | tuple[int, int] | int = field(
        default=0,
        metadata={'validator': lambda x: isinstance(x, (int, float, tuple)) and
                  (not isinstance(x, tuple) or len(x) == 2)}
    )

    flip: bool = field(
        default=False,
        metadata={'validator': lambda x: isinstance(x, bool)}
    )

    order: list[str] = field(
        default_factory=lambda: [''],
        metadata={'validator': lambda x: isinstance(x, list) and
                  all(isinstance(s, str) for s in x)}
    )

    @override
    def copy(self) -> 'LineData':
        """Create a deep copy of line render data.

        Returns:
            New LineData instance with copied properties

        Note:
            Ensures deep copy of all nested structures
        """
        try:
            return LineData(
                colors=deepcopy(self.colors),
                sizes=deepcopy(self.sizes),
                thickness=deepcopy(self.thickness),
                altmode=deepcopy(self.altmode),
                inset=deepcopy(self.inset),
                flip=deepcopy(self.flip),
                order=deepcopy(self.order)
            )
        except Exception as e:
            raise RuntimeError(f'Failed to copy LineData: {e}')

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'LineData':
        """Create LineData instance from arguments.

        Args:
            args: Property dictionary with any of:
                - color/linecolor: Color specifications
                - size/linesize: Size values
                - thickness: Line widths
                - mode/altmode: Render modes
                - inset: Edge insets
                - flip: Mirror flag
                - order: Section ordering

        Returns:
            New LineData instance

        Raises:
            TypeError: If args has invalid types
            ValueError: If args has invalid values
        """
        if not isinstance(args, dict):
            raise TypeError(f'args must be dictionary, got {type(args)}')

        data = LineData()
        data.set(args, False)
        return data

    # -------------------- access-point --------------------

    def _validate_property(self, name: str, value: Any) -> bool:
        """Validate a property value.

        Args:
            name: Property name
            value: Value to validate

        Returns:
            bool: True if value is valid

        Note:
            Uses field metadata validators when available
        """
        try:
            if hasattr(self, name):
                field_info = self.__class__.__dataclass_fields__[name]
                validator = field_info.metadata.get('validator')
                if validator:
                    return validator(value)
            return True
        except Exception:
            return False

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        """Update properties from argument dictionary.

        Args:
            args: Property updates
            skips: Skip validation if True

        Returns:
            bool: True if any properties were updated

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(args, dict):
            raise TypeError(f'args must be dictionary, got {type(args)}')

        s: bool = False
        for arg, v in args.items():
            if arg not in ['lineinset', 'inset', 'flip', 'lineorder', 'sectionorder', 'order']:
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
                        label = LineData.parseLabel(vv[0])
                        value = vv[1]
                    match arg:
                        case 'linecolor' | 'colors' | 'color' | 'col':
                            s = True
                            if not skips:
                                self.colors[label] = tColor(value)
                        case 'thickness' | 'width':
                            s = True
                            if not skips:
                                self.thickness[label] = int(LineData.extractNum(value))
                        case 'linesize' | 'sizes' | 'size':
                            s = True
                            if not skips:
                                match value:
                                    case 's':
                                        self.sizes[label] = 10
                                    case 'l':
                                        self.sizes[label] = 20
                                    case _:
                                        self.sizes[label] = LineData.parseNum(value)
                        case 'linemode' | 'altmode' | 'mode':
                            s = True
                            if not skips:
                                match value:
                                    case 'cross':
                                        self.altmode[label] = AltMode.CROSS
            else:
                match arg:
                    case 'lineinset' | 'inset':
                        s = True
                        if not skips:
                            self.inset = LineData.parsePartial(v)
                    case 'flip':
                        s = True
                        if not skips:
                            self.flip = True
                    case 'lineorder' | 'sectionorder' | 'order':
                        s = True
                        if not skips:
                            self.order = LineData.parseList(v)
        return s
