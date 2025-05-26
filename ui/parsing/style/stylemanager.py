import xml.etree.ElementTree as ET
from typing import Optional

class StyleManager:
    """
    StyleManager is a class to manage the render-data-requests for renderstyles    
    """

    styles: dict[str, dict[str, ET.Element]] = {}

    @staticmethod
    def addStyle(name: str, styledElements: dict[str, ET.Element]) -> None:
        StyleManager.styles[name] = styledElements
        
    @staticmethod
    def getStyledElement(element: str, stylename: str) -> Optional[ET.Element]:
        if stylename.lower() in StyleManager.styles:
            if element in StyleManager.styles[stylename]:
                return StyleManager.styles[stylename][element]
        return None
