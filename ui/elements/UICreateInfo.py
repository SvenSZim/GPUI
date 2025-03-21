from functools import partial
from typing import Any, Callable, Generic, TypeVar, Union

from .generic import Rect
from .simpleelements import UIABCBody
from .simpleelements import UILine, UILineCore, UISLine, UISLineCreateOptions
from .simpleelements import UIObject, UIObjectCore, UISObject, UISObjectCreateOptions
from .simpleelements import UIText, UITextCore, UISText, UISTextCreateOptions
from .simpleelements import UIButton, UIButtonCore, UISButton, UISButtonCreateOptions
from .UIRenderer import UIRenderer



Element = TypeVar('Element', bound=UIRenderer)

class UICreateInfo(Generic[Element]):

    _partial_constructor: partial

    @staticmethod
    def lineConstructor(body: Union[UIABCBody, Rect], active: bool = True, renderStyleData: Union[UISLine, list[UISLineCreateOptions]] = UISLine.SOLID) -> UILine:
        return UILine(UILineCore(body), active=active, renderStyleData=renderStyleData)

    @staticmethod
    def objectConstructor(body: Union[UIABCBody, Rect], active: bool = True, renderStyleData: Union[UISObject, list[UISObjectCreateOptions]] = UISObject.BASIC) -> UIObject:
        return UIObject(UIObjectCore(body), active=active, renderStyleData=renderStyleData)

    @staticmethod
    def textConstructor(body: Union[UIABCBody, Rect], content: str, active: bool = True, renderStyleData: Union[UISText, list[UISTextCreateOptions]] = UISText.BASIC) -> UIText:
        return UIText(UITextCore(body, content), active=active, renderStyleData=renderStyleData)

    @staticmethod
    def buttonConstructor(body: Union[UIABCBody, Rect], numberOfStates: int = 2, startState: int = 0,
                          active: bool = True, renderStyleData: Union[UISButton, list[UISButtonCreateOptions]] = UISButton.BASIC) -> UIButton:
        return UIButton(UIButtonCore(body, numberOfStates=numberOfStates, startState=startState), active=active, renderStyleData=renderStyleData)

    def __init__(self, constructor: type[Element], *pre_args: Any, **pre_kwargs: Any):
        if issubclass(constructor, UILine):
            self._partial_constructor = partial(UICreateInfo.lineConstructor, *pre_args, **pre_kwargs)
        elif issubclass(constructor, UIObject):
            self._partial_constructor = partial(UICreateInfo.objectConstructor, *pre_args, **pre_kwargs)
        elif issubclass(constructor, UIText):
            self._partial_constructor = partial(UICreateInfo.textConstructor, *pre_args, **pre_kwargs)
        elif issubclass(constructor, UIButton):
            self._partial_constructor = partial(UICreateInfo.buttonConstructor, *pre_args, **pre_kwargs)

    def createElement(self, *post_args: Any, **post_kwargs: Any) -> Element:
        return self._partial_constructor(*post_args, **post_kwargs)
