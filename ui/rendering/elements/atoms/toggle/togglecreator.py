
from ....style         import RenderStyle, StyleManager
from .togglecreateoption import ToggleCO
from .toggledata         import ToggleData

class ToggleCreator:
    """
    ToggleCreator is a intern class for creating RenderInfomation from ToggleCreateOptions.
    """

    @staticmethod
    def createToggleData(createOptions: list[ToggleCO], style: RenderStyle) -> ToggleData:
        """
        createToggleData creates a ToggleData object from a list of createOptions and a given style.

        Args:
            createOptions (list[ToggleCO]): the createOptions to be applied
            style         (RenderStyle) : the style to be used

        Returns (ToggleData): the RenderData created from the given args
        """
        toggleData: ToggleData = ToggleData()

        for createOption in createOptions:
            match createOption:
                case ToggleCO.NOSTATE:
                    toggleData.stateDispColor = None
                case ToggleCO.STATE1:
                    toggleData.stateDispStyle = 1
                    if toggleData.stateDispColor is None:
                        toggleData.stateDispColor = StyleManager.getStyleColor(0, style)
                case ToggleCO.STATE2:
                    toggleData.stateDispStyle = 2
                    if toggleData.stateDispColor is None:
                        toggleData.stateDispColor = StyleManager.getStyleColor(0, style)
                case ToggleCO.STATE3:
                    toggleData.stateDispStyle = 3
                    if toggleData.stateDispColor is None:
                        toggleData.stateDispColor = StyleManager.getStyleColor(0, style)

                case ToggleCO.COLOR1:
                    toggleData.stateDispColor = StyleManager.getStyleColor(0, style)
                case ToggleCO.COLOR2:
                    toggleData.stateDispColor = StyleManager.getStyleColor(1, style)
        
        return toggleData
