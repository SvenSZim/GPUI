
from ....style          import RenderStyle, StyleManager
from .linecreateoptions import LineCO
from .linedata          import LineData

class LineCreator:
    """
    LineCreator is a intern class for creating RenderInfomation from LineCreateOptions.
    """

    @staticmethod
    def createLineData(createOptions: list[LineCO], style: RenderStyle) -> LineData:
        """
        createLineData creates a LineData object from a list of createOptions and a given style.

        Args:
            createOptions (list[LineCO]): the createOptions to be applied
            style         (RenderStyle) : the style to be used

        Returns (LineData): the RenderData created from the given args
        """
        lineData: LineData = LineData()

        for createOption in createOptions:
            if 0x021 <= createOption.value <= 0x030:
                lineData.partial = 0.1 * (createOption.value - 0x020)
            match createOption:
                case LineCO.TRANSPARENT:
                    lineData.mainColor = None
                case LineCO.SOLID:
                    lineData.doAlt = False
                    if lineData.mainColor is None:
                        lineData.mainColor = StyleManager.getStyleColor(0, style)
                case LineCO.DOTTED:
                    lineData.doAlt = True
                    if lineData.mainColor is not None and lineData.altColor is not None:
                        lineData.altColor = None
                    if lineData.altAbsLen is None:
                        lineData.altAbsLen = 10.0
                case LineCO.ALTERNATING:
                    lineData.doAlt = True
                    if lineData.mainColor is None:
                        lineData.mainColor = StyleManager.getStyleColor(0, style)
                    if lineData.altColor is None:
                        lineData.mainColor = StyleManager.getStyleColor(1, style)
                    if lineData.altAbsLen is None:
                        lineData.altAbsLen = 10.0

                case LineCO.NOFLIP:
                    lineData.flip = False
                case LineCO.FLIPPED:
                    lineData.flip = True
                
                case LineCO.COLOR1:
                    lineData.mainColor = StyleManager.getStyleColor(0, style)
                case LineCO.COLOR2:
                    lineData.mainColor = StyleManager.getStyleColor(1, style)

                case LineCO.PARTIAL_NOPARTIAL:
                    lineData.partial = 1.0

                case LineCO.ALTLENGTH10:
                    lineData.altAbsLen = 10.0
                case LineCO.ALTLENGTH20:
                    lineData.altAbsLen = 20.0

                case LineCO.ALTCOLOR1:
                    lineData.altColor = StyleManager.getStyleColor(0, style)
                case LineCO.ALTCOLOR2:
                    lineData.altColor = StyleManager.getStyleColor(1, style)
        
        return lineData
