from typing import override

from ......display      import Surface
from ......interaction  import InputManager, InputEvent,Clickable
from .....createinfo    import CreateInfo
from ....body           import LayoutManager
from ....element        import Element
from ..addon            import Addon

from .dropdowncore         import DropdownCore
from .dropdowndata         import DropdownData
from .dropdowncreateoption import DropdownCO
from .dropdownprefab       import DropdownPrefab

class Dropdown(Addon[Element, DropdownCore, DropdownData, DropdownCO, DropdownPrefab], Clickable):

    __outer: Element

    # -------------------- creation --------------------

    def __init__(self, outer: Element, *inner: Element | tuple[Element, float], verticalDropdown: bool=True, dropdownActive: bool=True, offset: int=0,
                 renderData: DropdownPrefab | list[DropdownCO] | DropdownData=DropdownPrefab.BASIC, active: bool = True) -> None:
        assert self._renderstyle is not None

        if isinstance(renderData, list):
            myData: DropdownData = DropdownData()
            for createOption in renderData:
                myData += (createOption, self._renderstyle)
            myData += (DropdownCO.CREATE, self._renderstyle)
            renderData = myData
        elif isinstance(renderData, DropdownPrefab):
            renderData = DropdownData() * (renderData, self._renderstyle)

        Clickable.__init__(self, active)
        Addon.__init__(self, DropdownCore(outer.getRect(), *inner, verticalDropdown=verticalDropdown, offset=offset, buttonActive=dropdownActive), renderData, active)
        
        self._core.addTriggerEvent(self._onclick)
        #Default trigger event: LEFTDOWN
        self.addTriggerEvent(InputManager.getEvent(InputEvent.LEFTDOWN))
        
        self.__outer = outer

        LayoutManager.addConnection((True, True), self.__outer.getCore().getBody(), self.getCore().getBody(), (0.0, 0.0), (0.0, 0.0))
        LayoutManager.addConnection((True, True), self.__outer.getCore().getBody(), self.getCore().getBody(), (1.0, 1.0), (1.0, 1.0), keepSizeFix=False)
    
    @staticmethod
    @override
    def fromCreateOptions(createOptions: list[DropdownCO]) -> CreateInfo['Dropdown']:
        """
        fromCreateOptions creates the element from createoptions.

        Args:
            createoptions (list[CreateOption]): the list of create-options to be used for creating

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Dropdown, renderData=createOptions)

    @staticmethod
    @override
    def fromPrefab(prefab: DropdownPrefab) -> CreateInfo['Dropdown']:
        """
        fromPrefab creates the element from a prefab.

        Args:
            prefab (Prefab): the prefab to be created

        Returns (creator for this class): createinfo for this class
        """
        return CreateInfo(Dropdown, renderData=prefab)

    # -------------------- rendering --------------------

    @override
    def render(self, surface: Surface) -> None:
        """
        render renders the UI-Element onto the given surface

        Args:
            surface (Surface): the surface the UIElement should be drawn on
        """
        assert self._drawer is not None

        if self._active:
            self.__outer.render(surface)

            if self._core.getCurrentToggleState():
                self.addPostRenderElement(self._core.getInner())
