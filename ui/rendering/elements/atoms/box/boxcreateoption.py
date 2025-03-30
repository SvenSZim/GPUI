
from ..atomcreateoption import AtomCreateOption

class BoxCO(AtomCreateOption):
    """
    BoxCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Box'.
    """
    
    #-----------------------------------

    # fill style
    FILL_NOFILL         = 0x100
    FILL_SOLID          = 0x101

    # fill enabled
    FILL_TOPLEFT        = 0x111
    FILL_TOPRIGHT       = 0x112
    FILL_BOTTOMLEFT     = 0x113
    FILL_BOTTOMRIGHT    = 0x114

    # fill color options
    FILL_COLOR1         = 0x121
    FILL_COLOR2         = 0x122
