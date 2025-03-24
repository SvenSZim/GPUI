from abc import ABC

from ..UICore import UICore
from .uibody import UIABCBody

class UIABCCore(UICore, ABC):
    """
    UIABC is the abstract base class for all UIElements.
    """

    _body: UIABCBody # A UIBody which contains the positioning of the UIElement

    def __init__(self, body: UIABCBody):
        """
        __init__ initializes the values of UIABC for the UIElement

        Args:
            body: Body (bound=UIABCBody) = the body value for the UIElement
        """
        self._body = body

    def getBody(self) -> UIABCBody:
        """
        getBody returns the body of the UIElements
        (should only be used to create references between the objects like in DynamicBody!)

        Returns:
            Body = the body of the UIElement
        """
        return self._body

    #DEBUG
    def setBody(self, body: UIABCBody) -> None:
        self._body = body
