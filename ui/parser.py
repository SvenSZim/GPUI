from typing import Any, Optional
import xml.etree.ElementTree as ET

from .rendering import Element, Line, Box, Text
from .rendering import Framed, Grouped, Dropdown

class Parser:

    __taggedElements: dict[str, Element]={}
    
    @staticmethod
    def __fromNode(node: ET.Element) -> Optional[Element]:
        newElement: Element

        childs: list[Element] = []
        for c in node:
            newEl = Parser.__fromNode(c)
            if newEl is not None:
                childs.append(newEl)

        attributes: dict[str, Any] = node.attrib
        match node.tag:
            case 'line' | 'l':
                newElement = Line.parseFromArgs(attributes)
            case 'box' | 'b':
                newElement = Box.parseFromArgs(attributes)
            case 'text' | 't':
                attributes['content'] = node.text
                newElement = Text.parseFromArgs(attributes)
            case 'framed' | 'fr' | 'f':
                attributes['inner'] = childs
                newElement = Framed.parseFromArgs(attributes)
            case 'group' | 'grouped' | 'gr' | 'g':
                if not len(childs):
                    return None
                attributes['inner'] = childs
                newElement = Grouped.parseFromArgs(attributes)
            case 'dropdown' | 'dpd':
                if not len(childs):
                    return None
                attributes['inner'] = childs
                newElement = Dropdown.parseFromArgs(attributes)

            case _:
                return None
        
        tagTags: list[str] = ['label', 'tag', 'id', 'name']
        if any([x in attributes for x in tagTags]):
            tagValue: str = attributes[tagTags[[x in attributes for x in tagTags].index(True)]]
            if tagValue in Parser.__taggedElements:
                raise ValueError(f'{tagValue=} appears twice!')
            Parser.__taggedElements[tagValue] = newElement
        return newElement




    @staticmethod
    def fromXML(path: str) -> Element:
        tree: ET.ElementTree = ET.parse(path)
        newEl = Parser.__fromNode(tree.getroot())
        if newEl is None:
            raise ValueError('Could not find root element!')
        return newEl
