from typing import Any, Optional
import xml.etree.ElementTree as ET

from ..interaction import EventManager

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
        styleTags: list[str] = Element.styleTags

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
                if len(childs) >= Line.getMinRequiredChildren():
                    newElement = Line.parseFromArgs(attributes)
            case 'box' | 'b':
                if len(childs) >= Box.getMinRequiredChildren():
                    newElement = Box.parseFromArgs(attributes)
            case 'text' | 't':
                if len(childs) >= Text.getMinRequiredChildren():
                    newElement = Text.parseFromArgs(attributes)
            case 'framed' | 'fr' | 'f':
                if len(childs) >= Framed.getMinRequiredChildren():
                    newElement = Framed.parseFromArgs(attributes)
            case 'group' | 'grouped' | 'gr' | 'g':
                if len(childs) >= Grouped.getMinRequiredChildren():
                    newElement = Grouped.parseFromArgs(attributes)
            case 'dropdown' | 'dpd':
                if len(childs) >= Dropdown.getMinRequiredChildren():
                    newElement = Dropdown.parseFromArgs(attributes)
            case 'button':
                if len(childs) >= Button.getMinRequiredChildren():
                    newElement = Button.parseFromArgs(attributes)
            case 'checkbox' | 'selector':
                if len(childs) >= Checkbox.getMinRequiredChildren():
                    newElement = Checkbox.parseFromArgs(attributes)
            case 'slider':
                if len(childs) >= Slider.getMinRequiredChildren():
                    newElement = Slider.parseFromArgs(attributes)
            case 'elementcycle' | 'cycle' | 'cyclebutton':
                if len(childs) >= ElementCycle.getMinRequiredChildren():
                    newElement = ElementCycle.parseFromArgs(attributes)
            case 'multiselect' | 'multi':
                if len(childs) >= Multiselect.getMinRequiredChildren():
                    newElement = Multiselect.parseFromArgs(attributes)
            case 'dropdownselect' | 'dropselect' | 'downselect' | 'dropsel' | 'dpds':
                if len(childs) >= Dropdownselect.getMinRequiredChildren():
                    newElement = Dropdownselect.parseFromArgs(attributes)
            case 'section' | 'sec' | 's':
                if len(childs) >= Section.getMinRequiredChildren():
                    newElement = Section.parseFromArgs(attributes)
            case _:
                if any([x in attributes for x in styleTags]):
                    styleValue: str = attributes[styleTags[[x in attributes for x in styleTags].index(True)]]
                    prefNode: Optional[ET.Element] = StyleManager.getStyledElementNode(node.tag.lower(), styleValue)
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
    def answerElementRequest() -> None:
        elementRequest: Optional[ET.Element] = Element.parserRequest
        if elementRequest is not None:
            Element.parserResponse = Parser.__fromNode(elementRequest)[0]

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


EventManager.quickSubscribe(Element.parserCallEvent, Parser.answerElementRequest)