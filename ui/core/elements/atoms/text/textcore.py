from typing import Any, override

from .....utility import Rect
from ..atomcore import AtomCore

class TextCore(AtomCore):
    """
    TextCore

    Core state container for the `Text` atom.

    Responsibilities
    - Store the immutable/semi-immutable content string for the element.
    - Provide simple accessors (`getContent`, `setContent`) and a `copy()`
      method for cloning core state when elements are duplicated.

    Usage
    - Instances are lightweight and serializable as part of element
      parsing operations. Heavy validation belongs to the surrounding
      `TextData` and element parsing code.
    """
    _content: str

    # -------------------- creation --------------------

    def __init__(self, content: str) -> None:
        if not isinstance(content, str):
            raise TypeError(f'content must be a str, got {type(content)}')
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
        if not isinstance(args, dict):
            raise TypeError('args must be a dict')
        if not isinstance(skips, bool):
            raise TypeError('skips must be a bool')

        s: bool = False
        for tag, value in args.items():
            match tag:
                case 'content':
                    s = True
                    if not skips:
                        if isinstance(value, str):
                            self._content = value
                        else:
                            raise TypeError('content expects a str')
        return s
