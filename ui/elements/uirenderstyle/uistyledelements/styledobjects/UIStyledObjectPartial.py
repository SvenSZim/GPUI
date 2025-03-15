from typing import Optional, Union, override

from ....generic import Color, Rect
from ....uidrawerinterface import UISurfaceDrawer, UISurface
from .UIABCStyledObject import UIABCStyledObject

class UIStyledObjectPartial(UIABCStyledObject):
    """
    UIStyledObjectPartial is a abstract styling object to render just a percentage of another styled object.
    (e.g. for partial underlines or fractional objects)
    """
    __styledobject: type[UIABCStyledObject]
    __partialPercentage: float
    def __init__(self, styledobject: type[UIABCStyledObject], partialPercentage: float,
                 drawBorder: tuple[bool, bool, bool, bool]=(True, True, True, True),
                 borderColor: Optional[Union[str, tuple[int, int, int], Color]]=None,
                 fillColor: Optional[Union[str, tuple[int, int, int], Color]]=None) -> None:
        super().__init__(drawBorder, borderColor, fillColor)
        self.__styledobject = styledobject
        self.__partialPercentage = partialPercentage

    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface, data: Rect) -> None:
        """
        render renders the rect depending on the render style of the refering object and the partial-percentage.
        """
        partial_size: tuple[int, int] = (int(data.width * self.__partialPercentage), int(data.height * self.__partialPercentage))
        delta_size: tuple[int, int] = (data.width - partial_size[0], data.height - partial_size[1])
        offset: tuple[int, int] = (int(delta_size[0]/2), int(delta_size[1]/2))
            
        partial_rect: Rect = Rect((data.left + offset[0], data.top + offset[1]), partial_size)

        if self._fillColor is not None:
            styledObj: UIABCStyledObject = self.__styledobject(fillColor=self._fillColor)
            styledObj.render(surfaceDrawer, surface, partial_rect)
        if self._borderColor is not None:
            if self._drawBorder[0]:
                styledObj: UIABCStyledObject = self.__styledobject(drawBorder=(True, False, False, False), borderColor=self._borderColor)
                styledObj.render(surfaceDrawer, surface, Rect((partial_rect.left, data.top), (partial_rect.width, data.height)))
            if self._drawBorder[1]:
                styledObj: UIABCStyledObject = self.__styledobject(drawBorder=(False, True, False, False), borderColor=self._borderColor)
                styledObj.render(surfaceDrawer, surface, Rect((data.left, partial_rect.top), (data.width, partial_rect.height)))
            if self._drawBorder[2]:
                styledObj: UIABCStyledObject = self.__styledobject(drawBorder=(False, False, True, False), borderColor=self._borderColor)
                styledObj.render(surfaceDrawer, surface, Rect((data.left, partial_rect.top), (data.width, partial_rect.height)))
            if self._drawBorder[3]:
                styledObj: UIABCStyledObject = self.__styledobject(drawBorder=(False, False, False, True), borderColor=self._borderColor)
                styledObj.render(surfaceDrawer, surface, Rect((partial_rect.left, data.top), (partial_rect.width, data.height)))
        



