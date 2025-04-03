
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

    # fill enabled
    FILL_TOPLEFT        = 0x1011
    FILL_TOPRIGHT       = 0x1012
    FILL_BOTTOMLEFT     = 0x1013
    FILL_BOTTOMRIGHT    = 0x1014

    # fill color options
    FILL_COLOR1         = 0x1021
    FILL_COLOR2         = 0x1022
