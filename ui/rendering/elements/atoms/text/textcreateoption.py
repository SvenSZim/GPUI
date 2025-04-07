
from ..atomcreateoption import AtomCreateOption

class TextCO(AtomCreateOption):
    """
    TextCO (CreateOption) is the storage class for all possible
    CreateOptions when creating a object from the atom 'Text'.
    """

    # text value range 0x2000 - 0x2FFF

    # text style
    NOTEXT          = 0x2000
    SOLID           = 0x2001

    # text size
    SIZEDYNAMIC     = 0x2010
    SIZE_XXS        = 0x2011
    SIZE_XS         = 0x2012
    SIZE_S          = 0x2013
    SIZE_MS         = 0x2014
    SIZE_SM         = 0x2015
    SIZE_M          = 0x2016
    SIZE_LM         = 0x2017
    SIZE_ML         = 0x2018
    SIZE_L          = 0x2019 
    SIZE_XL         = 0x201a
    SIZE_XXL        = 0x201b

    # text color
    COLOR1          = 0x2021
    COLOR2          = 0x2022

    # text positioning
    ALIGNCENTER     = 0x2040
    ALIGNLEFT       = 0x2041
    ALIGNRIGHT      = 0x2042
    ALIGNTOP        = 0x2043
    ALIGNBOTTOM     = 0x2044
