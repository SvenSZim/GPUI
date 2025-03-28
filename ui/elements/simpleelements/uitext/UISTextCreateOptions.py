from ..UIStylingABCCreateOptions import UIStylingABCCreateOptions

class UISTextCreateOptions(UIStylingABCCreateOptions):
    

    #-----------------------------------
    # border style
    BORDER_NOBORDER     = 0x000
    BORDER_SOLID        = 0x001
    
    # border enabled
    BORDER_TOP          = 0x011
    BORDER_LEFT         = 0x012
    BORDER_RIGHT        = 0x013
    BORDER_BOTTOM       = 0x014

    # border color options
    BORDER_COLOR1       = 0x021
    BORDER_COLOR2       = 0x022

    #-----------------------------------

    # fill style
    FILL_NOFILL         = 0x100
    FILL_SOLID          = 0x101

    # fill enabled
    FILL_TOPLEFT        = 0x111
    FILL_TOPRIGHT       = 0x112
    FILL_BOTTOMLEFT     = 0x113
    FILL_BOTTOMRIGHT    = 0x114

    # fill color options
    FILL_COLOR1         = 0x121
    FILL_COLOR2         = 0x122

    #-----------------------------------

    # text style
    TEXT_NOTEXT         = 0x200
    TEXT_SOLID          = 0x201

    # text size
    TEXT_STATIC         = 0x210
    TEXT_DYNAMIC        = 0x211

    # text color
    TEXT_COLOR1         = 0x221
    TEXT_COLOR2         = 0x222
