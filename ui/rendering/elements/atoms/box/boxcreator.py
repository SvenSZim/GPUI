
from ....style        import RenderStyle, StyleManager
from ..line           import LineCO
from .boxcreateoption import BoxCO
from .boxdata         import BoxData


class BoxCreator:
    """
    BoxCreator is a intern class for creating RenderInfomation from BoxCreateOptions.
    """

    @staticmethod
    def createBoxData(createOptions: list[BoxCO], style: RenderStyle) -> BoxData:
        """
        createBoxData creates a BoxData object from a list of createOptions and a given style.

        Args:
            createOptions (list[BoxCO]): the createOptions to be applied
            style         (RenderStyle) : the style to be used

        Returns (BoxData): the RenderData created from the given args
        """
        borderData: list[LineCO] = []
        objectData: BoxData = BoxData(borderData=borderData)

        for createOption in createOptions:
            match createOption:
                case BoxCO.BORDER_NOBORDER:
                    borderData.append(LineCO.TRANSPARENT)
                case BoxCO.BORDER_SOLID:
                    borderData.append(LineCO.SOLID)
                case BoxCO.BORDER_TOP:
                    objectData.doBorders = (True, objectData.doBorders[1], objectData.doBorders[2], objectData.doBorders[3])
                case BoxCO.BORDER_LEFT:
                    objectData.doBorders = (objectData.doBorders[0], True, objectData.doBorders[2], objectData.doBorders[3])
                case BoxCO.BORDER_RIGHT:
                    objectData.doBorders = (objectData.doBorders[0], objectData.doBorders[1], True, objectData.doBorders[3])
                case BoxCO.BORDER_BOTTOM:
                    objectData.doBorders = (objectData.doBorders[0], objectData.doBorders[1], objectData.doBorders[2], True)

                case BoxCO.BORDER_COLOR1:
                    borderData.append(LineCO.COLOR1)
                case BoxCO.BORDER_COLOR2:
                    borderData.append(LineCO.COLOR2)
                
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
        
        objectData.borderData = borderData
        return objectData
