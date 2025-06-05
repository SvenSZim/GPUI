import xml.etree.ElementTree as ET
from typing import Optional

from ...utility import StyledDefault

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
    def getDefault(tag: StyledDefault) -> Optional[ET.Element]:
        if StyleManager.defaultStyle in StyleManager.styles:
            return StyleManager.getStyledElementNode(str(tag), StyleManager.defaultStyle)
        return None
