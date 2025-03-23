from typing import Any, Callable, Union

from ...generic import Rect
from ...simpleelements import UIABCBody, UIStaticBody
from ...simpleelements import UIText, UITextCore, UISText
from ...simpleelements import UIButton, UIButtonCore, UISButton
from ...UIRenderer import UIRenderer
from ..UIABCComplexCore import UIABCComplexCore


def setContent(textobj: UIText, content: str):
    """
    setContent sets the content of a UITextElement to a new content.

    Args:
        textobj: UIABCTextRenderer = the textobject to be modified
        content: str = the new content to be set
    """
    textobj.updateContent(content)


class UICTextCycleButtonCore(UIABCComplexCore):
    
    __button: UIButton
    __buttonStates: list[str]

    def __init__(self, body: UIABCBody | Rect, contents: list[Union[str, tuple[str, str]]], styles: tuple[UISText, UISButton]=(UISText.BASIC, UISButton.INVISIBLE)) -> None:
        
        if len(contents) == 0:
            contents = ['']
        if isinstance(body, Rect):
            body = UIStaticBody(body)
        for idx, content in enumerate(contents):
            if isinstance(content, str):
                contents[idx] = (content, content)

        textStyle: UISText
        buttonStyle: UISButton
        textStyle, buttonStyle = styles

        core_elements: list[UIRenderer] = []
        text: UIText = UIText(UITextCore(body, contents[0][0]), renderStyleData=textStyle)
        
        core_elements.append(text)
        self.__button = UIButton(UIButtonCore(body, numberOfStates=len(contents), startState=0), renderStyleData=buttonStyle)
        core_elements.append(self.__button)

        self.__buttonStates = []
        for idx, content in enumerate(contents):
            self.__buttonStates.append(content[1])
            self.__button.subscribeToButtonEvent(idx, setContent, text, contents[(idx + 1) % len(contents)][0])

        super().__init__(core_elements)


    def subscribeToButtonEvent(self, state: str, f: Callable, *args: Any) -> bool:
        """
        subscribeToButtonEvent subscribes a Callback to the triggerEvent of the
        given buttonState of the UICycleButton.

        Args:
            state: str = the buttonState the Callback should be subscribed to
            f: Callable = the function that should be subscribed
            *args: Any = the potential arguments the function needs

        Returns:
            bool = returns if the subscription was successful
        """
        return self.__button.subscribeToButtonEvent(self.__buttonStates.index(state), f, *args)


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
