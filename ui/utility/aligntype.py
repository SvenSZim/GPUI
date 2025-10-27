from enum import Enum


class AlignType(Enum):
    """Enumeration defining UI element alignment types.

    Bit pattern: 0bI_VH_i_RL
    - I: Inner flag (0/1)
    - VH: Vertical/Horizontal position (00=Top/Left, 01=Middle, 10=Bottom/Right)
    - i: Inner flag (0/1)
    - RL: Right/Left alignment (00=Left, 01=Middle, 10=Right)

    Naming convention:
    - First letter: T(op)/M(iddle)/B(ottom)
    - Second letter: L(eft)/M(iddle)/R(ight)
    - i prefix: Inner alignment
    - i suffix: Inner alignment

    Examples:
        TL: Top-Left alignment
        MR: Middle-Right alignment
        iTL: Inner-Top-Left
        TiR: Top-Inner-Right
    """

    # Position masks
    VMASK = 0b0_11_0_00  # Vertical position mask
    HMASK = 0b0_00_0_11  # Horizontal position mask
    IMASK = 0b1_00_0_00  # Inverse mask
    NMASK = 0b0_00_1_00  # Inner mask

    # Basic alignments
    TL   = 0b0_00_0_00  # Top-Left
    TM   = 0b0_00_0_01  # Top-Middle
    TR   = 0b0_00_0_10  # Top-Right
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
        """Convert string to AlignType.

        Args:
            s: Alignment string (e.g. 'TL', 'MR', 'iTL')

        Returns:
            Matching AlignType or TL if invalid

        Examples:
            >>> AlignType.fromStr('TL')
            AlignType.TL
            >>> AlignType.fromStr('MR')
            AlignType.MR
            >>> AlignType.fromStr('invalid')
            AlignType.TL
        """
        if not isinstance(s, str):
            return AlignType.TL

        s = s.strip()
        parsedict: dict[str, 'AlignType'] = {
            'TL':AlignType.TL, 'TM':AlignType.TM, 'TR':AlignType.TR, 'ML':AlignType.ML, 'MM':AlignType.MM, 'MR':AlignType.MR, 'BL':AlignType.BL, 'BM':AlignType.BM, 'BR':AlignType.BR,
            'TiL':AlignType.TiL, 'TiM':AlignType.TiM, 'TiR':AlignType.TiR, 'MiL':AlignType.MiL, 'MiM':AlignType.MiM, 'MiR':AlignType.MiR, 'BiL':AlignType.BiL, 'BiM':AlignType.BiM, 'BiR':AlignType.BiR,
            'iTL':AlignType.iTL, 'iTM':AlignType.iTM, 'iTR':AlignType.iTR, 'iML':AlignType.iML, 'iMM':AlignType.iMM, 'iMR':AlignType.iMR, 'iBL':AlignType.iBL, 'iBM':AlignType.iBM, 'iBR':AlignType.iBR,
            'iTiL':AlignType.iTiL, 'iTiM':AlignType.iTiM, 'iTiR':AlignType.iTiR, 'iMiL':AlignType.iMiL, 'iMiM':AlignType.iMiM, 'iMiR':AlignType.iMiR, 'iBiL':AlignType.iBiL, 'iBiM':AlignType.iBiM, 'iBiR':AlignType.iBiR,
        }
        return parsedict.get(s, AlignType.TL)

    def is_inverse(self) -> bool:
        """Check if this is an inverse alignment.

        Returns:
            True if alignment is inverse (i-prefixed)
        """
        return bool(self.value & AlignType.IMASK)

    def is_inner(self) -> bool:
        """Check if this is an inner alignment.

        Returns:
            True if alignment is inner (i-suffixed)
        """
        return bool(self.value & AlignType.NMASK)

    def get_vertical(self) -> str:
        """Get vertical alignment component.

        Returns:
            'T'op, 'M'iddle, or 'B'ottom
        """
        v = (self.value & AlignType.VMASK) >> 2
        return {0: 'T', 1: 'M', 2: 'B'}[v]

    def get_horizontal(self) -> str:
        """Get horizontal alignment component.

        Returns:
            'L'eft, 'M'iddle, or 'R'ight
        """
        h = self.value & AlignType.HMASK
        return {0: 'L', 1: 'M', 2: 'R'}[h]

    def __str__(self) -> str:
        """Convert to human-readable string.

        Returns:
            Alignment string (e.g. 'Top-Left', 'Middle-Right')
        """
        v_align = {'T': 'Top', 'M': 'Middle', 'B': 'Bottom'}[self.get_vertical()]
        h_align = {'L': 'Left', 'M': 'Middle', 'R': 'Right'}[self.get_horizontal()]
        parts = []
        if self.is_inverse():
            parts.append('Inverse')
        parts.extend([v_align, h_align])
        if self.is_inner():
            parts.append('Inner')
        return '-'.join(parts)
