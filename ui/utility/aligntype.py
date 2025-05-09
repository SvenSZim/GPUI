from enum import Enum


class AlignType(Enum):
    TL   = 0b0_00_0_00
    TM   = 0b0_00_0_01
    TR   = 0b0_00_0_10
    ML   = 0b0_01_0_00
    MM   = 0b0_01_0_01
    MR   = 0b0_01_0_10
    BL   = 0b0_10_0_00
    BM   = 0b0_10_0_01
    BR   = 0b0_10_0_10
    TiL  = 0b0_00_1_00
    TiM  = 0b0_00_1_01
    TiR  = 0b0_00_1_10
    MiL  = 0b0_01_1_00
    MiM  = 0b0_01_1_01
    MiR  = 0b0_01_1_10
    BiL  = 0b0_10_1_00
    BiM  = 0b0_10_1_01
    BiR  = 0b0_10_1_10
    iTL  = 0b1_00_0_00
    iTM  = 0b1_00_0_01
    iTR  = 0b1_00_0_10
    iML  = 0b1_01_0_00
    iMM  = 0b1_01_0_01
    iMR  = 0b1_01_0_10
    iBL  = 0b1_10_0_00
    iBM  = 0b1_10_0_01
    iBR  = 0b1_10_0_10
    iTiL = 0b1_00_1_00
    iTiM = 0b1_00_1_01
    iTiR = 0b1_00_1_10
    iMiL = 0b1_01_1_00
    iMiM = 0b1_01_1_01
    iMiR = 0b1_01_1_10
    iBiL = 0b1_10_1_00
    iBiM = 0b1_10_1_01
    iBiR = 0b1_10_1_10

    @staticmethod
    def fromStr(s: str) -> 'AlignType':
        parsedict: dict[str, 'AlignType'] = {
            'TL':AlignType.TL, 'TM':AlignType.TM, 'TR':AlignType.TR, 'ML':AlignType.ML, 'MM':AlignType.MM, 'MR':AlignType.MR, 'BL':AlignType.BL, 'BM':AlignType.BM, 'BR':AlignType.BR,
            'TiL':AlignType.TiL, 'TiM':AlignType.TiM, 'TiR':AlignType.TiR, 'MiL':AlignType.MiL, 'MiM':AlignType.MiM, 'MiR':AlignType.MiR, 'BiL':AlignType.BiL, 'BiM':AlignType.BiM, 'BiR':AlignType.BiR,
            'iTL':AlignType.iTL, 'iTM':AlignType.iTM, 'iTR':AlignType.iTR, 'iML':AlignType.iML, 'iMM':AlignType.iMM, 'iMR':AlignType.iMR, 'iBL':AlignType.iBL, 'iBM':AlignType.iBM, 'iBR':AlignType.iBR,
            'iTiL':AlignType.iTiL, 'iTiM':AlignType.iTiM, 'iTiR':AlignType.iTiR, 'iMiL':AlignType.iMiL, 'iMiM':AlignType.iMiM, 'iMiR':AlignType.iMiR, 'iBiL':AlignType.iBiL, 'iBiM':AlignType.iBiM, 'iBiR':AlignType.iBiR,
        }
        if parsedict.get(s):
            return parsedict[s]
        return AlignType.TL
