from typing import override
from ...generic import Rect
from ..uielementbody import UIABCBody, UIStaticBody
from ..UIABCCore import UIABCCore

class UITextCore(UIABCCore[UIABCBody]):

    _content: str

    def __init__(self, body: UIABCBody | Rect, content: str) -> None:
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        super().__init__(body)
        self._content = content

        self.update()

    @override
    def update(self) -> None:
        self._body.update()
    
    def getContent(self) -> str:
        """
        getContent returns the text-content of the UIText.

        Returns:
            str = text-content of the UIText
        """
        return self._content

    def setContent(self, content: str) -> None:
        """
        setContent sets the text-content of the UIText to a new given text-content.

        Args:
            content: str = new text-content for the UIText
        """
        self._content = content
