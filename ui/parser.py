from typing import Any, Optional
import xml.etree.ElementTree as ET

from .rendering import Element, Line, Box, Text, Framed

class Parser:
    
    @staticmethod
    def __fromNode(node: ET.Element) -> Optional[Element]:
        childs: list[Element] = []
        for c in node:
            newEl = Parser.__fromNode(c)
            if newEl is not None:
                childs.append(newEl)

        attributes: dict[str, Any] = node.attrib
        match node.tag:
            case 'line':
                return Line.parseFromArgs(attributes)
            case 'box':
                return Box.parseFromArgs(attributes)
            case 'text':
                attributes['content'] = node.text
                return Text.parseFromArgs(attributes)
            case 'framed':
                types = [0 if isinstance(x, Line) else 1 if isinstance(x, Box) else 2 for x in childs]
                match len(childs):
                    case 0:
                        return None
                    case 1:
                        attributes['inner']   = childs[0]
                        attributes['fill']    = Box.parseFromArgs({})
                        attributes['border0'] = Line.parseFromArgs({})
                        attributes['border1'] = Line.parseFromArgs({})
                        attributes['border2'] = Line.parseFromArgs({})
                        attributes['border3'] = Line.parseFromArgs({})
                    case 2:
                        if 0 in types:
                            border = childs[types.index(0)]
                            assert isinstance(border, Line)
                            attributes['inner']   = childs[1 - types.index(0)]
                            attributes['fill']    = Box.parseFromArgs({})
                            attributes['border0'] = border
                            attributes['border1'] = border.copy()
                            attributes['border2'] = border.copy()
                            attributes['border3'] = border.copy()
                        elif 1 in types:
                            attributes['inner']   = childs[1 - types.index(1)]
                            attributes['fill']    = childs[types.index(1)]
                            attributes['border0'] = Line.parseFromArgs({})
                            attributes['border1'] = Line.parseFromArgs({})
                            attributes['border2'] = Line.parseFromArgs({})
                            attributes['border3'] = Line.parseFromArgs({})
                        else:
                            attributes['inner']   = childs[0]
                            attributes['fill']    = Box.parseFromArgs({})
                            attributes['border0'] = Line.parseFromArgs({})
                            attributes['border1'] = Line.parseFromArgs({})
                            attributes['border2'] = Line.parseFromArgs({})
                            attributes['border3'] = Line.parseFromArgs({})
                    case _:
                        if 2 in types:
                            attributes['inner'] = childs[types.index(2)]
                            if 1 in types:
                                attributes['fill'] = childs[types.index(1)]
                            else:
                                attributes['fill'] = Box.parseFromArgs({})
                        else:
                            match types.count(1):
                                case 0:
                                    return None
                                case 1:
                                    attributes['inner'] = childs[types.index(1)]
                                case _:
                                    bi = types.index(1)
                                    attributes['fill'] = childs[bi]
                                    attributes['inner'] = childs[bi + types[bi+1:].index(1) + 1]
                        match types.count(0):
                            case 1:
                                border = childs[types.index(0)]
                                assert isinstance(border, Line)
                                attributes['border0'] = border
                                attributes['border1'] = border.copy()
                                attributes['border2'] = border.copy()
                                attributes['border3'] = border.copy()
                            case 2:
                                bi = types.index(0)
                                border1 = childs[bi]
                                border2 = childs[bi + types[bi+1:].index(0) + 1]
                                assert isinstance(border1, Line) and isinstance(border2, Line)
                                attributes['border0'] = border1
                                attributes['border1'] = border1.copy()
                                attributes['border2'] = border2
                                attributes['border3'] = border2.copy()
                            case _:
                                b1i = types.index(0)
                                b2i = b1i + types[b1i+1:].index(0) + 1
                                attributes['border0'] = childs[b1i]
                                attributes['border1'] = childs[b2i]
                                attributes['border2'] = childs[b2i + types[b2i+1:].index(0) + 1]
                                attributes['border3'] = Line.parseFromArgs({})
                return Framed.parseFromArgs(attributes)



    @staticmethod
    def fromXML(path: str) -> Element:
        tree: ET.ElementTree = ET.parse(path)
        newEl = Parser.__fromNode(tree.getroot())
        if newEl is None:
            raise ValueError('Could not find root element!')
        return newEl
