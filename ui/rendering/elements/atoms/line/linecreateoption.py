
from ..atomcreateoption import AtomCreateOption

class LineCO(AtomCreateOption):
    """
    LineCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Line'.
    """

    # line value range 0x0000 - 0x0FFF
    
    # style
    TRANSPARENT  = 0x0000
    SOLID        = 0x0001
    DOTTED       = 0x0002
    ALTERNATING  = 0x0003

    # drawing options
    NOFLIP       = 0x0008
    FLIPPED      = 0x0009
    
    # color options
    COLOR1       = 0x0011
    COLOR2       = 0x0012

    # size options
    PARTIAL_NOPARTIAL = 0x0020
    PARTIAL_10   = 0x0021
    PARTIAL_20   = 0x0022
    PARTIAL_30   = 0x0023
    PARTIAL_40   = 0x0024
    PARTIAL_50   = 0x0025
    PARTIAL_60   = 0x0026
    PARTIAL_70   = 0x0027
    PARTIAL_80   = 0x0028
    PARTIAL_90   = 0x0029

    # alt length
    ALTLENGTH10  = 0x0035
    ALTLENGTH20  = 0x0036

    # alt color
    ALTCOLOR1    = 0x003a
    ALTCOLOR2    = 0x003b

