
from ..interactablecreateoption import InteractableCreateOption

class SliderCO(InteractableCreateOption):
    """
    SliderCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the addon 'Slider'.
    """

    # value range 0x10400 - 0x104ff

    CREATE              = 0x10400

    USEBOX              = 0x10401
    USELINE             = 0x10402
