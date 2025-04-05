
from ..interactablecreateoption import InteractableCreateOption

class CheckboxCO(InteractableCreateOption):
    """
    CheckboxCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the addon 'Checkbox'.
    """

    # value range 0x10200 - 0x102ff

    CREATE              = 0x10200

    USEBOX              = 0x10201
    USECROSS            = 0x10202
    USECROSS_TL         = 0x10203
    USECROSS_TR         = 0x10204
