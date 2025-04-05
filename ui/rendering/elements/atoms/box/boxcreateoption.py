
from ..atomcreateoption import AtomCreateOption

class BoxCO(AtomCreateOption):
    """
    BoxCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Box'.
    """

    # box value range: 0x1000 - 0x1FFF
    
    # fill style
    FILL_NOFILL         = 0x1000
    FILL_SOLID          = 0x1001
    FILL_ALT            = 0x1003

    # fill color options
    COLOR0              = 0x1020
    COLOR1              = 0x1021
    COLOR2              = 0x1022
    
    # size options
    PARTIAL_NOPARTIAL   = 0x1030
    PARTIAL_10          = 0x1031
    PARTIAL_20          = 0x1032
    PARTIAL_30          = 0x1033
    PARTIAL_40          = 0x1034
    PARTIAL_50          = 0x1035
    PARTIAL_60          = 0x1036
    PARTIAL_70          = 0x1037
    PARTIAL_80          = 0x1038
    PARTIAL_90          = 0x1039
    
    # alt mode
    ALTDEFAULT          = 0x1050
    ALTSTRIPED_V        = 0x1051
    ALTSTRIPED_H        = 0x1052
    ALTSTRIPED_D        = 0x1053
    ALTSTRIPED_DR       = 0x1054
    ALTCHECKERBOARD     = 0x1055

    # alt length
    ALTLENGTH10         = 0x1065
    ALTLENGTH20         = 0x1066

    # alt color
    ALTCOLOR0           = 0x106a
    ALTCOLOR1           = 0x106b
    ALTCOLOR2           = 0x106c
