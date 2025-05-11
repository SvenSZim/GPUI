from typing import Optional
import xml.etree.ElementTree as ET

from .rendering import Element, Line, Box, Text

class Parser:
    
    @staticmethod
    def fromXML(path: str) -> Element:
        tree: ET.ElementTree = ET.parse(path)

        def flattenTree(root):
            ret = [root]
            for child in root:
                ret.extend(flattenTree(child))
            return ret
        
        nodeStack = flattenTree(tree.getroot())
        elementStack: list[Optional[Element]] = [None for _ in nodeStack]

        for i in range(len(nodeStack)-1, -1, -1):
            currentNode = nodeStack[i]
            newEl = None
            match currentNode.tag:
                case 'line':
                    newEl = Line.parseFromArgs(currentNode.attrib)
                case 'box':
                    newEl = Box.parseFromArgs(currentNode.attrib)
                case 'text':
                    allAttr = currentNode.attrib
                    allAttr['content'] = str(currentNode.text).strip()
                    newEl = Text.parseFromArgs(currentNode.attrib)
            elementStack[i] = newEl

        assert isinstance(elementStack[0], Element)
        return elementStack[0]
