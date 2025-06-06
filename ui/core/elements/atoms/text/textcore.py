from typing import Any, override

from .....utility import Rect
from ..atomcore import AtomCore

class TextCore(AtomCore):
    """
    TextCore is the core object of the atom-element 'Text'.
    """
    _content: str

    # -------------------- creation --------------------

    def __init__(self, content: str) -> None:
        super().__init__(Rect())
        self._content = content

    @override
    def copy(self) -> 'TextCore':
        return TextCore(self._content)

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

    #-------------------- access-point --------------------

    @override
    def set(self, args: dict[str, Any], skips: bool) -> bool:
        s: bool = False
        for tag, value in args.items():
            match tag:
                case 'content':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._content = value
                        else:
                            raise ValueError('content expects a str')
        return s
