
from ..atomcreateoption import AtomCreateOption

class LineCO(AtomCreateOption):
    """
    LineCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Line'.
    """
    
    # style
    TRANSPARENT  = 0x000
    SOLID        = 0x001
    DOTTED       = 0x002
    ALTERNATING  = 0x003

    # drawing options
    NOFLIP       = 0x008
    FLIPPED      = 0x009
    
    # color options
    COLOR1       = 0x011
    COLOR2       = 0x012

    # size options
    PARTIAL_NOPARTIAL = 0x020
    PARTIAL_10   = 0x021
    PARTIAL_20   = 0x022
    PARTIAL_30   = 0x023
    PARTIAL_40   = 0x024
    PARTIAL_50   = 0x025
    PARTIAL_60   = 0x026
    PARTIAL_70   = 0x027
    PARTIAL_80   = 0x028
    PARTIAL_90   = 0x029

    # alt length
    ALTLENGTH10  = 0x035
    ALTLENGTH20  = 0x036

    # alt color
    ALTCOLOR1    = 0x3a
    ALTCOLOR2    = 0x3b

