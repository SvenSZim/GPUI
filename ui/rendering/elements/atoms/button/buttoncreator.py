
from ....style         import RenderStyle, StyleManager
from .buttoncreateoption import ButtonCO
from .buttondata         import ButtonData

class ButtonCreator:
    """
    ButtonCreator is a intern class for creating RenderInfomation from ButtonCreateOptions.
    """

    @staticmethod
    def createButtonData(createOptions: list[ButtonCO], style: RenderStyle) -> ButtonData:
        """
        createButtonData creates a ButtonData object from a list of createOptions and a given style.

        Args:
            createOptions (list[ButtonCO]): the createOptions to be applied
            style         (RenderStyle) : the style to be used

        Returns (ButtonData): the RenderData created from the given args
        """
        buttonData: ButtonData = ButtonData()

        for createOption in createOptions:
            match createOption:
                case ButtonCO.NOSTATE:
                    buttonData.stateDispColor = None
                case ButtonCO.STATE1:
                    buttonData.stateDispStyle = 1
                    if buttonData.stateDispColor is None:
                        buttonData.stateDispColor = StyleManager.getStyleColor(0, style)
                case ButtonCO.STATE2:
                    buttonData.stateDispStyle = 2
                    if buttonData.stateDispColor is None:
                        buttonData.stateDispColor = StyleManager.getStyleColor(0, style)
                case ButtonCO.STATE3:
                    buttonData.stateDispStyle = 3
                    if buttonData.stateDispColor is None:
                        buttonData.stateDispColor = StyleManager.getStyleColor(0, style)

                case ButtonCO.COLOR1:
                    buttonData.stateDispColor = StyleManager.getStyleColor(0, style)
                case ButtonCO.COLOR2:
                    buttonData.stateDispColor = StyleManager.getStyleColor(1, style)
        
        return buttonData
