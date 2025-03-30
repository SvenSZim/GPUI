
from ..atomcreateoption import AtomCreateOption

class TextCO(AtomCreateOption):
    """
    TextCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Text'.
    """

    #-----------------------------------

    # text style
    NOTEXT         = 0x200
    SOLID          = 0x201

    # text size
    STATIC         = 0x210
    DYNAMIC        = 0x211

    # text color
    COLOR1         = 0x221
    COLOR2         = 0x222
