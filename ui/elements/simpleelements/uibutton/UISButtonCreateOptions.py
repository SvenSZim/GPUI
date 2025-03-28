from ..UIStylingABCCreateOptions import UIStylingABCCreateOptions

class UISButtonCreateOptions(UIStylingABCCreateOptions):
    

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

    # button style
    BUTTON_NOSTATE      = 0x200
    BUTTON_STATE1       = 0x201
    BUTTON_STATE2       = 0x202
    BUTTON_STATE3       = 0x203

    # button color
    BUTTON_COLOR1       = 0x221
    BUTTON_COLOR2       = 0x222
