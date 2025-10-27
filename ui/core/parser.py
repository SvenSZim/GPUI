from typing import Any, Optional
import xml.etree.ElementTree as ET

from ..interaction import EventManager

from .style import StyleManager

from .elements import Element, Line, Box, Text
from .elements import Framed, Grouped, Dropdown
from .elements import Button, Toggle, Slider, Multiselect, Dropdownselect
from .elements import Section, UI

class Parser:

    @staticmethod
    def loadLayoutFromXML(path: str) -> UI:
        """Load and parse a UI layout from an XML file.

        Args:
            path (str): Path to the XML layout file

        Returns:
            UI: The parsed UI tree

        Raises:
            ValueError: If no valid root element is found
            ET.ParseError: If XML is malformed
        """
        tree = ET.parse(path)
        root = tree.getroot()
        if root is None:
            raise ValueError('XML file contains no root element')
        newEl, rawNamedElements = Parser.__fromNode(root)
        if newEl is None:
            raise ValueError('Failed to parse root element from XML layout file')
        if not isinstance(newEl, UI):
            namedElements = {k:v[1] for k, v in rawNamedElements.items()}
            return UI.parseFromArgs({'inner':[newEl], 'named': namedElements})
        return newEl

    @staticmethod
    def loadStyleFromXML(path: str) -> None:
        """Load style definitions from an XML file into the StyleManager.
        
        Args:
            path (str): Path to the XML style file
            
        Raises:
            ET.ParseError: If XML is malformed
        """
        tree = ET.parse(path)
        root = tree.getroot()
        if root is None:
            raise ValueError('XML file contains no root element')
        Parser.__fromNode(root)

    @staticmethod
    def getAllStyles() -> list[str]:
        return StyleManager.getAllStyles()

    @staticmethod
    def setDefaultStyle(style: str) -> bool:
        return StyleManager.setDefaultStyle(style)

    
    # -------------------- parsing --------------------


    __namedElements: dict[str, Element]={}

    @staticmethod
    def __fromNode(node: ET.Element) -> tuple[Optional[Element], dict[str, tuple[ET.Element, Element]]]:
        # -------------------- setup --------------------
        idTags   : list[str] = ['label', 'tag', 'id', 'name']
        styleTags: list[str] = Element.styleTags

        def getID(attributes: dict[str, Any], tags: list[str], usedTags: set[str] | None = None) -> Optional[str]:
            """
            getID extracts the first matching identifier from attributes using the
            provided tags list. If usedTags is provided the found id is checked
            for duplicates and an error is raised when a duplicate is encountered.

            Args:
                attributes: attribute dict from the parsed XML node
                tags: ordered list of keys to check for an id
                usedTags: optional set of already-used ids to validate uniqueness

            Returns:
                The found id string or None if no id key is present.
            """
            if usedTags is None:
                usedTags = set()
            if any([x in attributes for x in tags]):
                tagValue: str = attributes[tags[[x in attributes for x in tags].index(True)]]
                if tagValue in usedTags:
                    raise ValueError(f'{tagValue=} appears twice!')
                return tagValue
            return None

        # -------------------- rec-parsing --------------------
        attributes: dict[str, Any] = node.attrib

        namedElements: dict[str, tuple[ET.Element, Element]] = {}

        children: list[Element] = []
        for c in node:
            newEl, subNamedElement = Parser.__fromNode(c)
            if newEl is not None:
                children.append(newEl)
            if len(namedElements) + len(subNamedElement) != len(set(namedElements).union(subNamedElement)):
                raise ValueError(f'labels={set(namedElements).intersection(subNamedElement)} appear twice!')
            namedElements |= subNamedElement
        attributes['inner'] = children

        # -------------------- styles --------------------
        if node.tag.lower() in styleTags:
            if len(namedElements):
                newStyle: Optional[str] = getID(attributes, idTags)
                if newStyle:
                    StyleManager.addStyle(newStyle, {k:v[0] for k, v in namedElements.items()})
            return None, {}

        # -------------------- elements --------------------
        attributes['content'] = node.text.strip() if node.text is not None else ''
        if any([x in attributes for x in styleTags]):
            attributes['fixstyle'] = attributes[styleTags[[x in attributes for x in styleTags].index(True)]]
        else:
            attributes['fixstyle'] = StyleManager.defaultStyle


        newElement: Optional[Element] = None
        match node.tag.lower():
            case 'line' | 'l':
                if len(children) >= Line.getMinRequiredChildren():
                    newElement = Line.parseFromArgs(attributes)
            case 'box' | 'b':
                if len(children) >= Box.getMinRequiredChildren():
                    newElement = Box.parseFromArgs(attributes)
            case 'text' | 't':
                if len(children) >= Text.getMinRequiredChildren():
                    newElement = Text.parseFromArgs(attributes)
            case 'framed' | 'fr' | 'f':
                if len(children) >= Framed.getMinRequiredChildren():
                    newElement = Framed.parseFromArgs(attributes)
            case 'group' | 'grouped' | 'gr' | 'g':
                if len(children) >= Grouped.getMinRequiredChildren():
                    newElement = Grouped.parseFromArgs(attributes)
            case 'dropdown' | 'dpd':
                if len(children) >= Dropdown.getMinRequiredChildren():
                    newElement = Dropdown.parseFromArgs(attributes)
            
            case 'button':
                if len(children) >= Button.getMinRequiredChildren():
                    newElement = Button.parseFromArgs(attributes)
            
            case 'checkbox' | 'selector':
                attributes['typ'] = 'checkbox'
                if len(children) >= Toggle.getMinRequiredChildren():
                    newElement = Toggle.parseFromArgs(attributes)
            case 'elementcycle' | 'cycle' | 'cyclebutton':
                attributes['typ'] = 'cycle'
                if len(children) >= Toggle.getMinRequiredChildren():
                    newElement = Toggle.parseFromArgs(attributes)

            case 'slider':
                if len(children) >= Slider.getMinRequiredChildren():
                    newElement = Slider.parseFromArgs(attributes)
            case 'multiselect' | 'multi':
                if len(children) >= Multiselect.getMinRequiredChildren():
                    newElement = Multiselect.parseFromArgs(attributes)
            case 'dropdownselect' | 'dropselect' | 'downselect' | 'dropsel' | 'dpds':
                if len(children) >= Dropdownselect.getMinRequiredChildren():
                    newElement = Dropdownselect.parseFromArgs(attributes)
            case 'section' | 'sec' | 's':
                if len(children) >= Section.getMinRequiredChildren():
                    newElement = Section.parseFromArgs(attributes)
            case 'ui':
                if len(children) >= UI.getMinRequiredChildren():
                    attributes['named'] = {k:v[1] for k, v in namedElements.items()}
                    newElement = UI.parseFromArgs(attributes)

            case _:
                styleValue: str = StyleManager.defaultStyle
                if any([x in attributes for x in styleTags]):
                    styleValue: str = attributes[styleTags[[x in attributes for x in styleTags].index(True)]]
                prefNode: Optional[ET.Element] = StyleManager.getStyledElementNode(node.tag.lower(), styleValue)
                if prefNode:
                    prefElement: Optional[Element] = Parser.__fromNode(prefNode)[0]
                    if prefElement is not None:
                        newElement = prefElement
        if newElement is None:
            return None, {}

        # -------------------- post-parsing --------------------
        if 'text' in attributes:
            for i, txt in enumerate(Element.parseList(attributes['text'])):
                if len(txt):
                    newElement.set({'content':txt}, sets=1, skips=[i])

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
    def getElementByID(id: str) -> Element:
        """Retrieve a UI element by its ID.
        
        Args:
            id (str): The ID of the element to find
            
        Returns:
            Element: The element with the specified ID
            
        Raises:
            ValueError: If no element exists with the given ID
        """
        if id in Parser.__namedElements:
            return Parser.__namedElements[id]
        raise ValueError(f'No UI element found with ID "{id}". Available IDs: {list(Parser.__namedElements.keys())}')


EventManager.quickSubscribe(Element.parserCallEvent, Parser.answerElementRequest)
