from os import path as os_path
from json import load as json_load
import xml.etree.ElementTree as ET
from typing import Optional

DEFAULTS: dict[str, str] = {}
filepath: str = os_path.join(os_path.dirname(os_path.abspath(__file__)), 'defaults.json')
with open(filepath,'r') as file:
    DEFAULTS = json_load(file)

class StyleManager:
    """
    StyleManager is a class to manage the render-data-requests for renderstyles    
    """

    styles: dict[str, dict[str, ET.Element]] = {}
    
    defaultStyle: str = ''

    @staticmethod
    def addStyle(name: str, styledElements: dict[str, ET.Element]) -> None:
        StyleManager.styles[name] = styledElements

    @staticmethod
    def getAllStyles() -> list[str]:
        return list(StyleManager.styles.keys())

    @staticmethod
    def setDefaultStyle(style: str) -> bool:
        if style in StyleManager.styles:
            StyleManager.defaultStyle = style
            return True
        return False

    @staticmethod
    def getStyledElementNode(element: str, stylename: str) -> Optional[ET.Element]:
        if stylename.lower() in StyleManager.styles:
            if element in StyleManager.styles[stylename]:
                return StyleManager.styles[stylename][element]
        return None

    @staticmethod
    def getDefault(tag: str) -> Optional[ET.Element]:
        if StyleManager.defaultStyle in StyleManager.styles and tag in DEFAULTS:
            return StyleManager.getStyledElementNode(DEFAULTS[tag], StyleManager.defaultStyle)
        return None
