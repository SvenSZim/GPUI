
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
    
    # alt mode
    ALTDEFAULT          = 0x1030
    ALTSTRIPED_V        = 0x1031
    ALTSTRIPED_H        = 0x1032
    ALTSTRIPED_D        = 0x1033
    ALTSTRIPED_DR       = 0x1034
    ALTCHECKERBOARD     = 0x1035

    # alt length
    ALTLENGTH10         = 0x1045
    ALTLENGTH20         = 0x1046

    # alt color
    ALTCOLOR0           = 0x104a
    ALTCOLOR1           = 0x104b
    ALTCOLOR2           = 0x104c
