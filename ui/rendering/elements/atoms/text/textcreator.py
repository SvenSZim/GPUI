
from ....style         import RenderStyle, StyleManager
from .textcreateoption import TextCO
from .textdata         import TextData

class TextCreator:
    """
    TextCreator is a intern class for creating RenderInfomation from TextCreateOptions.
    """

    # #################### CLASS-METHODS ####################

    @staticmethod
    def createTextData(createOptions: list[TextCO], style: RenderStyle) -> TextData:
        """
        createTextData creates a TextData object from a list of createOptions and a given style.

        Args:
            createOptions (list[TextCO]): the createOptions to be applied
            style         (RenderStyle) : the style to be used

        Returns (TextData): the RenderData created from the given args
        """
        textData: TextData = TextData()

        for createOption in createOptions:
            match createOption:
                case TextCO.NOTEXT:
                    textData.textColor = None
                case TextCO.SOLID:
                    if textData.textColor is None:
                        textData.textColor = StyleManager.getStyleColor(0, style)

                case TextCO.STATIC:
                    textData.dynamicText = False
                    if textData.fontSize is None:
                        textData.fontSize = 24
                case TextCO.DYNAMIC:
                    textData.dynamicText = True
                    textData.fontSize = None

                case TextCO.COLOR1:
                    textData.textColor = StyleManager.getStyleColor(0, style)
                case TextCO.COLOR2:
                    textData.textColor = StyleManager.getStyleColor(1, style)
        
        return textData
