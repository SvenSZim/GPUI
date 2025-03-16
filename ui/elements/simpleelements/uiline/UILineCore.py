

from ..UIABCCore import UIABCCore

Point = tuple[int, int]
Edge = tuple[Point, Point]

class UILineCore(UIABCCore[Edge]):
    
    def __init__(self, body: Edge):
        super().__init__(body)
