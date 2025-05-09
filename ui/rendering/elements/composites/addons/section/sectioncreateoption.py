
from ..addoncreateoption import AddonCreateOption

class SectionCO(AddonCreateOption):
    """
    SectionCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the addon 'Section'.
    """

    # value range 0xa000 - 0xa7ff

    USEBORDER_HEADER    = 0xa001
    USEBORDER_FOOTER    = 0xa002
    USEBORDER_DEFAULT   = 0xa003
