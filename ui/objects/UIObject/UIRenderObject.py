from dataclasses import dataclass
from .UIObject import UIObject

@dataclass
class UIObjectRenderInfo:
    borders: tuple[bool, bool, bool, bool] | bool = False

class UIRenderObject:

    body: UIObject
    renderInfo: UIObjectRenderInfo

    def __init__(self, body: UIObject, renderInfo: UIObjectRenderInfo) -> None:
        self.body = body
        self.renderInfo = renderInfo

    def getBody(self) -> UIObject:
        return self.body

    def getRenderInfo(self) -> UIObjectRenderInfo:
        return self.renderInfo
