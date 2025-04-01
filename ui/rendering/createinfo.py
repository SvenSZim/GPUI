from functools import partial
from typing import Any, Generic, TypeVar

from .renderer import Renderer



Element = TypeVar('Element', bound=Renderer)

class CreateInfo(Generic[Element]):

    _partial_constructor: partial

    def __init__(self, element: type[Element], *pre_args: Any, **pre_kwargs: Any):
        self._partial_constructor = partial(element, *pre_args, **pre_kwargs)

    def createElement(self, *post_args: Any, **post_kwargs: Any) -> Element:
        return self._partial_constructor(*post_args, **post_kwargs)
