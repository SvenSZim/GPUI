from typing import Union

from ..UIABC import UIABC
from .UILineCore import UILineCore
from .UILineRenderData import UILineRenderData

class UILine(UIABC[UILineCore, UILineRenderData]):

    def __init__(self, core: UILineCore, active: bool, renderData: UILineRenderData) -> None:
        super().__init__(core, active, renderData)
