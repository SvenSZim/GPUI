from abc import ABC, abstractmethod
from typing import Any, Optional

from .color import Color, tColor


class Parsable(ABC):
    
    @staticmethod
    def parseBinary(s: str) -> int:
        nn = ''
        for c in s:
            if c == '0' or c == '1':
                nn += c
        if len(nn) > 0:
            return int(nn, 2)
        return 0

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
    def parseNum(s: str) -> int | float:
        if '.' in s:
            vk, nk = list(map(Parsable.extractNum, s.split('.')))[:2]
            return int(vk) + int(nk)/10**len(nk)
        return int(Parsable.extractNum(s))

    @staticmethod
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

    @staticmethod
    def parseFilterArgs(s: str) -> tuple[float, float, tuple[float, float]]:
        s = s.strip()
        n = len(s)
        if not n:
            return (0.0, 0.0, (0.0, 0.0))
        content = s
        if '(' in s and ')' in s:
            i = s.index('(')
            j = n-1 - s[::-1].index(')')
            if j > i:
                content = s[i+1:j]
        l = [v for v in Parsable.parseList(content)]
        match len(l):
            case 1:
                return (Parsable.parseNum(l[0]), 0.0, (0.0, 0.0))
            case 2:
                return (Parsable.parseNum(l[0]), Parsable.parseNum(l[1]), (0.0, 0.0))
            case _:
                if '+' in l[2]:
                    u, v = [Parsable.parseNum(m) for m in l[2].split('+')][:2]
                    return (Parsable.parseNum(l[0]), Parsable.parseNum(l[1]), (u, v))
                elif l[2][-1] == 'y':
                    return (Parsable.parseNum(l[0]), Parsable.parseNum(l[1]), (0.0, Parsable.parseNum(l[2])))
                else:
                    return (Parsable.parseNum(l[0]), Parsable.parseNum(l[1]), (Parsable.parseNum(l[2]), 0.0))

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
            x, y = list(map(Parsable.parseNum, s.split(',')))[:2]
            return (x, y)
        else:
            return Parsable.parseNum(s)

    @staticmethod
    def parseColor(s: str) -> Optional[Color]:
        if not len(s):
            return None
        s = s.strip()
        if s[0] == '(':
            vals = [v.strip() for v in s[1:-1].split(',')]
            if len(vals) > 2 and all([v.isnumeric() for v in vals]):
                return (int(vals[0]),int(vals[1]),int(vals[2]))
        else:
            s = s.lower()
            if tColor.is_valid_color(s):
                return s
            if s in ['none', 'inv']:
                return None
        raise ValueError(f'Unparsable color: {s}!')

    @staticmethod
    def adjustList(l: list[str], adjustments: list[str]) -> list[str]:
        currentIdx = 0
        for adj in adjustments:
            if '=' in adj:
                jumpToStr, value = adj.split('=')
                jumpTo = int(Parsable.extractNum(jumpToStr)) - 1
                if jumpTo < len(l):
                    currentIdx = jumpTo
                adj = value
            if currentIdx < len(l):
                l[currentIdx] = adj
            currentIdx += 1
        return l


    @staticmethod
    def parsePartition(s: str) -> tuple[int, int, list[str]]:
        size, *rem = s.split(';')
        x: int = 1
        y: int = 1
        for c in ['x', '*', '-', '/']:
            if c in size:
                x, y = list(map(int, size.split(c)))[:2]
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
                    cont = Parsable.parseList(labels[i:labels[i:].index(']')+i+1])
                    if crow < y:
                        ret[2][crow*x:(crow+1)*x] = Parsable.adjustList(ret[2][crow*x:(crow+1)*x], cont)
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

