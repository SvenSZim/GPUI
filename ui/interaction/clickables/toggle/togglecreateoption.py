
from ..atomcreateoption import AtomCreateOption

class ToggleCO(AtomCreateOption):
    """
    ToggleCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Toggle'.
    """

    #-----------------------------------

    # toggle style
    NOSTATE      = 0x200
    STATE1       = 0x201
    STATE2       = 0x202
    STATE3       = 0x203

    # toggle color
    COLOR1       = 0x221
    COLOR2       = 0x222
