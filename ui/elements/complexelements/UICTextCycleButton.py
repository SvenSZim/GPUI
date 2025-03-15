
from typing import Any, Callable
from ui.responsiveness import InputEvent, InputManager

from ..uidrawerinterface import UIFont
from ..uirenderstyle import UIStyledObjects, UIStyledTexts
from ..simpleelements import UIABCRenderer
from ..simpleelements import UIABCBody
from ..simpleelements import UIObjectRenderer
from ..simpleelements import UIText, UIABCTextRenderer, UIStaticTextRenderer, UIDynamicTextRenderer
from ..simpleelements import UICycleButton, UICycleButtonRenderer
from .UIABCComplex import UIABCComplex

def setContent(textobj: UIABCTextRenderer, content: str):
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

    __button_core: UICycleButton

    def __init__(self, body: UIABCBody, contents: list[str], fontData: tuple[UIFont | tuple[str, int] | str, str]) -> None:
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

        core_elements: list[UIABCRenderer] = []

        core_elements.append(UIObjectRenderer(body, renderStyleElement=UIStyledObjects.BASIC_25))

        txt: UIText = UIText(body, contents[0])
        text_core: UIABCTextRenderer
        if isinstance(fontData[0], str):
            text_core = UIDynamicTextRenderer(txt, fontData[0], fontData[1], renderStyleElement=UIStyledTexts.BASIC_NOBORDER)
            core_elements.append(text_core)
        else:
            text_core = UIStaticTextRenderer(txt, fontData[0], fontData[1], renderStyleElement=UIStyledTexts.BASIC_NOBORDER)
            core_elements.append(text_core)

        self.__button_core = UICycleButton(body, numberOfStates=len(contents))
        core_elements.append(UICycleButtonRenderer(self.__button_core, active=False))
        
        self.__button_core.addTriggerEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN))
        for x in range(len(contents)):
            self.__button_core.subscribeToButtonEvent(x, setContent, text_core, contents[(x + 1) % len(contents)])

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
        return self.__button_core.subscribeToButtonEvent(state, f, *args)


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
        return self.__button_core.subscribeToButtonClick(f, *args)



