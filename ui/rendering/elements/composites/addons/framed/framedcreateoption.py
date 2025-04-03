
from ..addoncreateoption import AddonCreateOption

class FramedCO(AddonCreateOption):
    """
    FramedCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the addon 'Framed'.
    """

    # value range 0x8000 - 0x87ff

    CREATE              = 0x8000

    USEBORDER_L         = 0x8001
    USEBORDER_R         = 0x8002
    USEBORDER_LR        = 0x8003
    USEBORDER_T         = 0x8004
    USEBORDER_LT        = 0x8005
    USEBORDER_RT        = 0x8006
    USEBORDER_LRT       = 0x8007
    USEBORDER_B         = 0x8008
    USEBORDER_LB        = 0x8009
    USEBORDER_RB        = 0x800a
    USEBORDER_LRB       = 0x800b
    USEBORDER_TB        = 0x800c
    USEBORDER_LTB       = 0x800d
    USEBORDER_RTB       = 0x800e
    USEBORDER_DEFAULT   = 0x800f
