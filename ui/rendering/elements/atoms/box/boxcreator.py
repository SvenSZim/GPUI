
from ....style        import RenderStyle, StyleManager
from .boxcreateoption import BoxCO
from .boxdata         import BoxData


class BoxCreator:
    """
    BoxCreator is a intern class for creating RenderInfomation from BoxCreateOptions.
    """

    # #################### CLASS-METHODS ####################

    @staticmethod
    def createBoxData(createOptions: list[BoxCO], style: RenderStyle) -> BoxData:
        """
        createBoxData creates a BoxData object from a list of createOptions and a given style.

        Args:
            createOptions (list[BoxCO]): the createOptions to be applied
            style         (RenderStyle) : the style to be used

        Returns (BoxData): the RenderData created from the given args
        """
        objectData: BoxData = BoxData()

        for createOption in createOptions:
            match createOption:
                case BoxCO.FILL_NOFILL:
                    objectData.fillColor = None
                case BoxCO.FILL_SOLID:
                    objectData.doAlt = False
                    if objectData.fillColor is None:
                        objectData.fillColor = StyleManager.getStyleColor(0, style)
                
                case BoxCO.FILL_TOPLEFT:
                    pass
                case BoxCO.FILL_TOPRIGHT:
                    pass
                case BoxCO.FILL_BOTTOMLEFT:
                    pass
                case BoxCO.FILL_BOTTOMRIGHT:
                    pass

                case BoxCO.FILL_COLOR1:
                    objectData.fillColor = StyleManager.getStyleColor(0, style)
                case BoxCO.FILL_COLOR2:
                    objectData.fillColor = StyleManager.getStyleColor(1, style)
        
        return objectData
