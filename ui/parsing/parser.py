from typing import Any, Optional
import xml.etree.ElementTree as ET

from .style import StyleManager

from .elements import Element, Line, Box, Text
from .elements import Framed, Grouped, Dropdown
from .elements import Button, Checkbox, Slider, ElementCycle, Multiselect, Dropdownselect
from .elements import Section

class Parser:

    __namedElements: dict[str, Element]={}
    
    @staticmethod
    def __fromNode(node: ET.Element) -> tuple[Optional[Element], dict[str, tuple[ET.Element, Element]]]:
        # -------------------- setup --------------------
        idTags   : list[str] = ['label', 'tag', 'id', 'name']
        styleTags: list[str] = ['style', 'styled', 'styleid', 'styledid']

        def getID(attributes: dict[str, Any], tags: list[str], usedTags: set[str]=set()) -> Optional[str]:
            if any([x in attributes for x in tags]):
                tagValue: str = attributes[tags[[x in attributes for x in tags].index(True)]]
                if tagValue in usedTags:
                    raise ValueError(f'{tagValue=} appears twice!')
                return tagValue
            return None

        # -------------------- rec-parsing --------------------
        attributes: dict[str, Any] = node.attrib

        namedElements: dict[str, tuple[ET.Element, Element]] = {}

        childs: list[Element] = []
        for c in node:
            newEl, subNamedElement = Parser.__fromNode(c)
            if newEl is not None:
                childs.append(newEl)
            if len(namedElements) + len(subNamedElement) != len(set(namedElements).union(subNamedElement)):
                raise ValueError(f'labels={set(namedElements).intersection(subNamedElement)} appear twice!')
            namedElements |= subNamedElement
        attributes['inner'] = childs
        
        # -------------------- styles --------------------
        if node.tag.lower() in styleTags:
            if len(namedElements):
                newStyle: Optional[str] = getID(attributes, idTags)
                if newStyle:
                    StyleManager.addStyle(newStyle, {k:v[0] for k, v in namedElements.items()})
            return None, {}

        # -------------------- elements --------------------
        newElement: Optional[Element] = None
        attributes['content'] = node.text.strip() if node.text is not None else ''
        match node.tag.lower():
            case 'line' | 'l':
                newElement = Line.parseFromArgs(attributes)
            case 'box' | 'b':
                newElement = Box.parseFromArgs(attributes)
            case 'text' | 't':
                newElement = Text.parseFromArgs(attributes)
            case 'framed' | 'fr' | 'f':
                newElement = Framed.parseFromArgs(attributes)
            case 'group' | 'grouped' | 'gr' | 'g':
                if len(childs):
                    newElement = Grouped.parseFromArgs(attributes)
            case 'dropdown' | 'dpd':
                if len(childs):
                    newElement = Dropdown.parseFromArgs(attributes)
            case 'button':
                newElement = Button.parseFromArgs(attributes)
            case 'checkbox':
                newElement = Checkbox.parseFromArgs(attributes)
            case 'slider':
                newElement = Slider.parseFromArgs(attributes)
            case 'elementcycle' | 'cycle' | 'cyclebutton':
                if len(childs):
                    newElement = ElementCycle.parseFromArgs(attributes)
            case 'multiselect' | 'multi':
                if len(childs):
                    newElement = Multiselect.parseFromArgs(attributes)
            case 'dropdownselect' | 'dropselect' | 'downselect' | 'dropsel' | 'dpds':
                if len(childs) > 1:
                    newElement = Dropdownselect.parseFromArgs(attributes)
            case 'section' | 'sec' | 's':
                if len(childs):
                    newElement = Section.parseFromArgs(attributes)
            case _:
                if any([x in attributes for x in styleTags]):
                    styleValue: str = attributes[styleTags[[x in attributes for x in styleTags].index(True)]]
                    prefNode: Optional[ET.Element] = StyleManager.getStyledElement(node.tag.lower(), styleValue)
                    if prefNode:
                        prefElement: Optional[Element] = Parser.__fromNode(prefNode)[0]
                        if prefElement is not None:
                            newElement = prefElement
        if newElement is None:
            return None, {}

        # -------------------- id --------------------
        newID: Optional[str] = getID(attributes, idTags, set(namedElements))
        if newID:
            namedElements[newID] = (node, newElement)
        
        return newElement, namedElements




    @staticmethod
    def fromXML(path: str) -> Element:
        tree: ET.ElementTree = ET.parse(path)
        newEl, namedElements = Parser.__fromNode(tree.getroot())
        if newEl is None:
            raise ValueError('Could not find root element!')
        Parser.__namedElements = {k:v[1] for k, v in namedElements.items()}
        return newEl

    @staticmethod
    def getElementByID(id: str) -> Element:
        if id in Parser.__namedElements:
            return Parser.__namedElements[id]
        raise ValueError(f'{id=} does not exist')
