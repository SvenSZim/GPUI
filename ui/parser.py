from typing import Any, Optional
from copy import deepcopy
import xml.etree.ElementTree as ET

from .rendering import Element, Line, Box, Text, Framed

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
        allAttr: dict[str, Any]

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
                case 'framed':
                    allAttr = currentNode.attrib
                    inners = [x.tag.strip().lower() for x in currentNode]
                    bc = False
                    lc = []
                    for idx, tag in enumerate(inners):
                        match tag:
                            case 'box':
                                if not bc:
                                    allAttr['fill'] = elementStack[i+idx+1]
                                    bc = True
                            case 'line':
                                if len(lc) < 4:
                                    allAttr[f'border{len(lc)}'] = elementStack[i+idx+1]
                                    lc.append(i+idx+1)
                            case _:
                                allAttr['inner'] = elementStack[i+idx+1]
                    if not bc:
                        allAttr['fill'] = Box.parseFromArgs({})
                    match len(lc):
                        case 0 | 3:
                            for j in range(len(lc), 4):
                                allAttr[f'border{j}'] = Line.parseFromArgs({})
                        case 1:
                            for j in range(len(lc), 4):
                                allAttr[f'border{j}'] = Line.parseFromArgs(nodeStack[lc[0]].attrib)
                        case 2:
                            allAttr['border3'] = allAttr['border1']
                            allAttr['border1'] = deepcopy(allAttr['border0'])
                            allAttr['border4'] = deepcopy(allAttr['border3'])
                            
                    newEl = Framed.parseFromArgs(allAttr)
                        
            elementStack[i] = newEl

        assert isinstance(elementStack[0], Element)
        return elementStack[0]
