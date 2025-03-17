
from typing import Any, Callable, Optional

from ..generic import Rect
from ..simpleelements import UIABCBody, UIStaticBody
from ..simpleelements import UISObject, UISText, UISButton
from ..simpleelements import UIText, UITextCore, UIButton, UIButtonCore
from ..UIRenderer import UIRenderer
from .UIABCComplex import UIABCComplex

def setContent(textobj: UIText, content: str):
    """
    setContent sets the content of a UITextElement to a new content.

    Args:
        textobj: UIABCTextRenderer = the textobject to be modified
        content: str = the new content to be set
    """
    textobj.updateContent(content)


class UICTextCycleButton(UIABCComplex):
    """
    UICTextCycleButton is a complex UIElement which consists of a button and a text where
    the text rotates through a list of strings by the press of the button.
    """

    __button: UIButton

    def __init__(self, body: UIABCBody | Rect, contents: list[str], styles: Optional[tuple[UISText, UISButton]]=None) -> None:
        """
        __init__ initializes the UICTextCycleButton object.

        Args:
            body: UIABCBody = the position and size of the UICTextCycleButton object.
            contents: list[str] = the texts to cycle through.
            fontData: ... = the needed font data for rendering. 
                                EITHER the direct font (UIFont) or the name and font size ~ StaticText
                                OR just the font name ~ DynamicText
                            plus the font color
        """
        if len(contents) == 0:
            contents = ['']
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        if styles is None:
            styles = (UISText.BASIC, UISButton.INVISIBLE)

        objectStyle: UISObject
        textStyle: UISText
        buttonStyle: UISButton
        textStyle, buttonStyle = styles

        core_elements: list[UIRenderer] = []
        text: UIText = UIText(UITextCore(body, contents[0]), renderStyleData=textStyle)
        core_elements.append(text)
        self.__button = UIButton(UIButtonCore(body, numberOfStates=len(contents), startState=0), renderStyleData=buttonStyle)
        core_elements.append(self.__button)

        for x in range(len(contents)):
            self.__button.subscribeToButtonEvent(x, setContent, text, contents[(x + 1) % len(contents)])

        super().__init__(core_elements)



    def subscribeToButtonEvent(self, state: int, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonEvent subscribes a Callback to the triggerEvent of the
        given buttonState of the UICycleButton.

        Args:
            state: int = the buttonState the Callback should be subscribed to
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscription was successful
        """
        return self.__button.subscribeToButtonEvent(state, f, *args)


    def subscribeToButtonClick(self, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonClick subscribes a Callback to the triggerEvent of
        all buttonStates of the UICycleButton.

        Args:
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscriptions were successful
        """
        return self.__button.subscribeToButtonClick(f, *args)



