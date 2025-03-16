from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


Body = TypeVar('Body', bound=Any)

class UIABCCore(Generic[Body], ABC):
    """
    UIABC is the abstract base class for all UIElements.
    """

    _body: Body # A UIBody which contains the positioning of the UIElement

    def __init__(self, body: Body):
        """
        __init__ initializes the values of UIABC for the UIElement

        Args:
            body: Body (bound=UIABCBody) = the body value for the UIElement
        """
        self._body = body

    def getBody(self) -> Body:
        """
        getBody returns the body of the UIElements
        (should only be used to create references between the objects like in DynamicBody!)

        Returns:
            Body = the body of the UIElement
        """
        return self._body

    @abstractmethod
    def update(self) -> None:
        pass

