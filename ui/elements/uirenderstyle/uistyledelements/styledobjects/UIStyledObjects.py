from enum import Enum

from ..UIStyledElements import UIStyledElements


class UIStyledObjects(UIStyledElements, Enum):

    # Objects from 0x100 to 0x1FF
    BASIC = 0x100
    BASIC_90 = 0x101
    BASIC_75 = 0x102
    BASIC_50 = 0x103
    BASIC_25 = 0x104
    BASIC_10 = 0x105
