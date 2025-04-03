
from ..atomcreateoption import AtomCreateOption

class TextCO(AtomCreateOption):
    """
    TextCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Text'.
    """

    # text value range 0x2000 - 0x2FFF

    # text style
    NOTEXT         = 0x2000
    SOLID          = 0x2001

    # text size
    STATIC         = 0x2010
    DYNAMIC        = 0x2011

    # text color
    COLOR1         = 0x2021
    COLOR2         = 0x2022
