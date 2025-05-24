from enum import Enum

class InputEvent(Enum):
    # ---------- digital-events ----------
    NONE = 0
    QUIT = 1

    WINDOW_RESIZE   = 12

    MOUSEBUTTONDOWN = 100
    MOUSEBUTTONUP   = 101

    LEFTDOWN        = 104
    LEFTUP          = 105
    RIGHTDOWN       = 106
    RIGHTUP         = 107

    A_DOWN      = 200
    A_UP        = 201
    B_DOWN      = 202
    B_UP        = 203
    C_DOWN      = 204
    C_UP        = 205
    D_DOWN      = 206
    D_UP        = 207
    E_DOWN      = 208
    E_UP        = 209
    F_DOWN      = 210
    F_UP        = 211
    G_DOWN      = 212
    G_UP        = 213
    H_DOWN      = 214
    H_UP        = 215
    I_DOWN      = 216
    I_UP        = 217
    J_DOWN      = 218
    J_UP        = 219
    K_DOWN      = 220
    K_UP        = 221
    L_DOWN      = 222
    L_UP        = 223
    M_DOWN      = 224
    M_UP        = 225
    N_DOWN      = 226
    N_UP        = 227
    O_DOWN      = 228
    O_UP        = 229
    P_DOWN      = 230
    P_UP        = 231
    Q_DOWN      = 232
    Q_UP        = 233
    R_DOWN      = 234
    R_UP        = 235
    S_DOWN      = 236
    S_UP        = 237
    T_DOWN      = 238
    T_UP        = 239
    U_DOWN      = 240
    U_UP        = 241
    V_DOWN      = 242
    V_UP        = 243
    W_DOWN      = 244
    W_UP        = 245
    X_DOWN      = 246
    X_UP        = 247
    Y_DOWN      = 248
    Y_UP        = 249
    Z_DOWN      = 250
    Z_UP        = 251

    
    # ---------- analog-events ----------
    UPDATE = 1000
    LEFTHELD = 1100

    @staticmethod
    def fromStr(s: str) -> 'InputEvent':
        if not len(s):
            return InputEvent.NONE
        s = s.lower()[0]
        if ord('a') <= ord(s) <= ord('z'):
            return InputEvent(2*(ord(s) - ord('a')) + 200)
        return InputEvent.NONE
