import json, os
from typing import Any

class StyleManager:
    """
    StyleManager is a class to manage the render-data-requests for renderstyles    
    """

    styles: dict[str, dict[str, Any]] = {}

    @staticmethod
    def loadStyle(path: str, stylename: str='') -> None:
        if not len(stylename):
            stylename = os.path.basename(path)
        with open(path,'r') as file:
            StyleManager.styles[stylename] = json.load(file)
        
    @staticmethod
    def getStyledElement(element: str, stylename: str) -> tuple[bool, dict[str, Any]]:
        if stylename in StyleManager.styles:
            if element in StyleManager.styles[stylename]:
                return ('DEPTH' in StyleManager.styles[stylename][element]), StyleManager.styles[stylename][element]
        return False, {}


StyleManager.loadStyle(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styleexample.json'))
