from dataclasses import dataclass
from typing import Any, override

from ......utility  import AlignType
from ....element    import Element
from ....atoms      import Line, Box
from ..addondata    import AddonData

@dataclass
class FramedData(AddonData):
    """
    FramedData is the storage class for all render-information
    for the addon 'Framed'.
    """
    fillData    : Box
    borderData  : tuple[Line, Line, Line, Line]

    def alignInner(self, against: Element) -> None:
        self.fillData.align(against)
        self.fillData.alignSize(against)
        self.borderData[0].align(against)
        self.borderData[0].align(against, AlignType.iBL, keepSize=False)
        self.borderData[1].align(against, AlignType.iTiR)
        self.borderData[1].align(against, AlignType.iBR, keepSize=False)
        self.borderData[2].align(against)
        self.borderData[2].align(against, AlignType.TiR, keepSize=False)
        self.borderData[3].align(against, AlignType.iBiL)
        self.borderData[3].align(against, AlignType.BiR, keepSize=False)

    @staticmethod
    @override
    def parseFromArgs(args: dict[str, Any]) -> 'FramedData':
        inner: list[Element] = args['inner']
        types = [0 if isinstance(x, Line) else 1 if isinstance(x, Box) else 2 for x in inner]
        match len(inner):
            case 0:
                raise ValueError("Insufficient amount of children in Framed!")
            case 1:
                return FramedData(Box.parseFromArgs({}), (Line.parseFromArgs({}), Line.parseFromArgs({}), Line.parseFromArgs({}), Line.parseFromArgs({})))
            case 2:
                if 0 in types:
                    border = inner[types.index(0)]
                    assert isinstance(border, Line)
                    return FramedData(Box.parseFromArgs({}), (border, border.copy(), border.copy(), border.copy()))
                elif 1 in types:
                    fill = inner[types.index(1)]
                    assert isinstance(fill, Box)
                    return FramedData(fill, (Line.parseFromArgs({}), Line.parseFromArgs({}), Line.parseFromArgs({}), Line.parseFromArgs({})))
                else:
                    return FramedData(Box.parseFromArgs({}), (Line.parseFromArgs({}), Line.parseFromArgs({}), Line.parseFromArgs({}), Line.parseFromArgs({})))
            case _:
                fill = Box.parseFromArgs({})
                if 1 not in types and 2 not in types:
                    raise ValueError("No frameable children in Framed!")
                elif 2 not in types and types.count(1) > 1 or 2 in types and 1 in types:
                    fill = inner[types.index(1)]
                assert isinstance(fill, Box)
                border1 = Line.parseFromArgs({})
                border2 = Line.parseFromArgs({})
                border3 = Line.parseFromArgs({})
                border4 = Line.parseFromArgs({})
                if types.count(0) > 0:
                    border1 = inner[types.index(0)]
                    if types.count(0) > 1:
                        border2 = inner[types.index(0, types.index(0)+1)]
                        if types.count(0) > 2:
                            border3 = inner[types.index(0, types.index(0, types.index(0)+1)+1)]
                            if types.count(0) > 3:
                                border4 = inner[types.index(0, types.index(0, types.index(0, types.index(0)+1)+1)+1)]
                        else:
                            assert isinstance(border1, Line) and isinstance(border2, Line)
                            return FramedData(fill, (border1, border1.copy(), border2, border2.copy()))
                    else:
                        assert isinstance(border1, Line)
                        return FramedData(fill, (border1, border1.copy(), border1.copy(), border1.copy()))
                assert isinstance(border1, Line) and isinstance(border2, Line) and isinstance(border3, Line) and isinstance(border4, Line)
                return FramedData(fill, (border1, border2, border3, border4))
