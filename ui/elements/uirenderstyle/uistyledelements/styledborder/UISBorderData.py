from dataclasses import dataclass
from enum import Enum

from ..UIStyledElementData import UIStylingElementOptions, UIStyledElementData

class UISBorderOptions(UIStylingElementOptions, Enum):
    
    # borderData (0x100 - 0x1FF)

    # borderEnabledData (0x110 - 0x11F):

    NOBORDER    = 0x110 # 0000
    BORDER_B    = 0x111 # 0001
    BORDER_R    = 0x112 # 0010
    BORDER_RB   = 0x113 # 0011
    BORDER_L    = 0x114 # 0100
    BORDER_LB   = 0x115 # 0101
    BORDER_LR   = 0x116 # 0110
    BORDER_LRB  = 0x117 # 0111
    BORDER_T    = 0x118 # 1000
    BORDER_TB   = 0x119 # 1001
    BORDER_TR   = 0x11a # 1010
    BORDER_TRB  = 0x11b # 1011
    BORDER_TL   = 0x11c # 1100
    BORDER_TLB  = 0x11d # 1101
    BORDER_TLR  = 0x11e # 1110
    FULLBORDER  = 0x11f # 1111

    # borderPartialData (0x120 - 0x12F):

    BORDER_00   = 0x120
    BORDER_10   = 0x121
    BORDER_20   = 0x122
    BORDER_30   = 0x123
    BORDER_40   = 0x124
    BORDER_50   = 0x125
    BORDER_60   = 0x126
    BORDER_70   = 0x127
    BORDER_80   = 0x128
    BORDER_90   = 0x129
    BORDER_100  = 0x12a

    # borderLineStyle (0x130 - 0x13F):

    BORDER_SOLID    = 0x130
    BORDER_DOTTED   = 0x131




    

@dataclass
class UISBorderData(UIStyledElementData):
    borderEnabledData: UISBorderOptions=UISBorderOptions.FULLBORDER
    borderPartialData: UISBorderOptions=UISBorderOptions.BORDER_100
    borderLineStyle: UISBorderOptions=UISBorderOptions.BORDER_SOLID



    
