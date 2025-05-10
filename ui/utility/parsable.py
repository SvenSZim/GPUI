from abc import ABC, abstractmethod
from typing import Any, Optional

from .color import Color

def parseList(s: str, separator: str=',') -> list[str]:
    ret: list[str] = []
    s = s.strip()
    n = len(s)
    if not n:
        return ret
    content = s
    if '[' in s and ']' in s:
        i = s.index('[')
        j = n-1 - s[::-1].index(']')
        if j > i:
            content = s[i+1:j]
    return [s.strip() for s in content.split(separator)]



class Parsable(ABC):

    @staticmethod
    def extractNum(s: str) -> str:
        nn = ''
        for c in s:
            if c.isnumeric():
                nn += c
        if len(nn) > 0:
            return nn
        return '0'

    @staticmethod
    def parseLabel(s: str) -> str:
        s = s.strip()
        if s[0].isnumeric():
            raise ValueError(f'Label {s} begins with a number!')
        forbidden: list[str] = ['=', ':', '[', ']', '{', '}']
        if any([c in s for c in forbidden]):
            raise ValueError(f'Label {s} contains a forbidden char: {forbidden}')
        return s

    @staticmethod
    def parsePartial(s: str) -> tuple[float, float] | float | tuple[int, int] | int:
        s = s.strip()
        if ',' in s:
            return (0,0)
        else:
            if '.' in s:
                vk, nk = [Parsable.extractNum(x) for x in s.split('.')][:2]
                return int(vk) + int(nk) / 10**len(nk)
            else:
                return int(Parsable.extractNum(s))

    @staticmethod
    def parseColor(s: str) -> Optional[Color]:
        s = s.strip()
        if s[0] == '(':
            vals = [v.strip() for v in s[1:-1].split(',')]
            if len(vals) > 2 and all([v.isnumeric() for v in vals]):
                return (int(vals[0]),int(vals[1]),int(vals[2]))
        else:
            s = s.lower()
            if s in ['white', 'black', 'red', 'green', 'blue']:
                return s
            if s in ['none', 'inv']:
                return None
        raise ValueError(f'Unparsable color: {s}!')

    @staticmethod
    def parsePartition(s: str) -> tuple[int, int, list[str]]:
        size, *rem = s.split(';')
        x: int = 1
        y: int = 1
        for c in ['x', '*', '-', '/']:
            if c in size:
                x, y = list(map(lambda x: int(x), size.split(c)))[:2]
        x, y = max(1, x), max(1, y)
        ret: tuple[int, int, list[str]] = (x, y, ['' for _ in range(x * y)])
        if len(rem) > 0:
            labels = rem[0].strip()
            i, n = 0, len(labels)
            cnum = ''
            crow = 0
            while i < n:
                c = labels[i]
                if c == '[':
                    cont = parseList(labels[i:labels[i:].index(']')+i+1])
                    rr = 0
                    for c in cont:
                        z = c
                        if '=' in c:
                            ci, l = c.split('=')
                            ri = int(Parsable.extractNum(ci)) - 1
                            if ri < x:
                                rr = ri
                            z = l
                        if rr < x and crow < y:
                            ret[2][crow * x + rr] = z
                        rr += 1
                    crow += 1
                    i = labels[i:].index(']') + i
                elif c.isnumeric():
                    cnum += c
                elif c == '=':
                    if len(cnum) > 0:
                        nn = int(cnum)
                        cnum = ''
                        if nn <= y:
                            crow = nn - 1
                i += 1
        return ret


    @staticmethod
    @abstractmethod
    def parseFromArgs(args: dict[str, Any]) -> 'Parsable':
        pass

