from typing import override

from .....utility import Rect
from ..atomcore import AtomCore

class TextCore(AtomCore):
    """
    TextCore is the core object of the atom-element 'Text'.
    """
    _content: str

    # -------------------- creation --------------------

    def __init__(self, rect: Rect, content: str) -> None:
        super().__init__(rect)
        self._content = content

    @override
    def copy(self) -> 'TextCore':
        return TextCore(Rect(), self._content)

    # -------------------- content --------------------
    
    def getContent(self) -> str:
        """
        getContent returns the text-content of the Text.

        Returns (str): text-content of the Text
        """
        return self._content

    def setContent(self, content: str) -> None:
        """
        setContent sets the text-content of the Text to a new given text-content.

        Args:
            content (str): new text-content for the Text
        """
        self._content = content
