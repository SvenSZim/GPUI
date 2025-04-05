
from ..interactablecreateoption import InteractableCreateOption

class ButtonCO(InteractableCreateOption):
    """
    ButtonCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the addon 'Button'.
    """

    # value range 0x10100 - 0x101ff

    CREATE              = 0x10100

    USEBOX              = 0x10101
    USECROSS            = 0x10102
    USECROSS_TL         = 0x10103
    USECROSS_TR         = 0x10104
