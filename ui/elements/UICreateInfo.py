from functools import partial
from typing import Any, Generic, TypeVar

from .UIRenderer import UIRenderer



Element = TypeVar('Element', bound=UIRenderer)

class UICreateInfo(Generic[Element]):

    _partial_constructor: partial

    def __init__(self, constructor: type[Element], *pre_args: Any, **pre_kwargs: Any):
        self._partial_constructor = partial(constructor.constructor, *pre_args, **pre_kwargs)

    def createElement(self, *post_args: Any, **post_kwargs: Any) -> Element:
        return self._partial_constructor(*post_args, **post_kwargs)
