from typing import override
from ...generic import Rect
from ..uielementbody import UIABCBody, UIStaticBody
from ..UIABCCore import UIABCCore

class UIObjectCore(UIABCCore[UIABCBody]):

    def __init__(self, body: UIABCBody | Rect) -> None:
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        super().__init__(body)
        self.update()

    @override
    def update(self) -> None:
        self._body.update()
