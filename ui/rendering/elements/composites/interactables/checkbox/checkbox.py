
from ......utility import Rect
from ....element   import Element
from .checkboxcore import CheckboxCore
from .checkboxdata import CheckboxData

class Checkbox(Element[CheckboxCore, CheckboxData]):

    def __init__(self, rect: Rect, renderData: CheckboxData, active: bool = True) -> None:

        super().__init__(core, renderData, active)

