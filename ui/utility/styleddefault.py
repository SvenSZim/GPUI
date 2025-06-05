from enum import Enum


class StyledDefault(Enum):
    # -------------------- ATOMS --------------------
    LINE        = 0x010
    BORDER      = 0x011
    BOX         = 0x020
    BACKGROUND  = 0x021
    TEXT        = 0x030

    # -------------------- ADDONS --------------------
    FRAMED      = 0x110
    TEXTBOX     = 0x111

    # -------------------- INTERACT --------------------
    BUTTON_ON       = 0x210
    BUTTON_OFF      = 0x211
    BUTTON_DEF      = 0x214
    BUTTON_TXT      = 0x215

    CHECKBOX_ON     = 0x220
    CHECKBOX_OFF    = 0x221
    CHECKBOX_DEF    = 0x224
    CHECKBOX_TXT    = 0x225

    def __str__(self) -> str:
        s = super().__str__()
        return s[s.index('.')+1:].lower()
