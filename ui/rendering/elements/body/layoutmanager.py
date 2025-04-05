from dataclasses import dataclass

from ....utility import iRect
from .body import Body

Point = tuple[float, float]

@dataclass
class Joint:
    """
    Joint is a dataclass to store the connection for a Body object
    """
    dimension: tuple[bool, bool]
    start: tuple[int, Point]
    end: tuple[int | iRect, Point]
    offset: int | tuple[int, int]=0
    fixedGlobal: tuple[bool, bool]=(True, True)
    keepSizeFix: tuple[bool, bool]=(True, True)

class LayoutManager:
    """
    LayoutManager is a 'static' class for managing the layout composition
    of the UI. It references all Body objects and applys layout-actions to them.
    """

    # #################### CLASS-METHODS ####################

    __l_bodys: list[Body] = []
    __l_joints: list[Joint] = []

    @staticmethod
    def addBody(body: Body) -> int:
        """
        addBody registeres a newly created Body object to the LayoutManager.

        Args:
            body (Body): the new Body object to register

        Returns (int): the index of the new Body in the LayoutManager
        """
        LayoutManager.__l_bodys.append(body)
        return len(LayoutManager.__l_bodys) - 1

    @staticmethod
    def getBodyIdx(body: Body) -> int:
        """
        getBodyIdx returns the stored body-index for a given body

        Args:
            body (Body): the body to check for

        Returns (int): the stored body-index of the given body
        """
        return LayoutManager.__l_bodys.index(body)


    @staticmethod
    def addConnection(connectionDimension: tuple[bool, bool],
                      body: Body, fixTo: iRect, bodyFixPoint: Point, otherFixPoint: Point,
                      offset: int | tuple[int, int]=0, 
                      fixedGlobal: tuple[bool, bool] | bool=True,
                      keepSizeFix: tuple[bool, bool] | bool=True) -> None:
        """
        addConnection creates and adds a new connection between a body and a reference object
        to the layout.

        Args:
            connectionDimension (tuple[bool, bool]) ~ (x-axis, y-axis)  : the dimension of the new connection.
            body                (Body)                                  : the body the connection should apply to
            fixTo               (iRect)                                 : the reference object to use for connecting
            bodyFixPoint        (Point) ~ (tuple[float, float])         : the relative position in the body to fix
            otherFixPoint       (Point) ~ (tuple[float, float])         : the relative position in the reference object to use as absolute position
            offset              (int or tuple[int, int])                : a offset to use when connecting. int applies to both dimensions
            fixedGlobal         (tuple[bool, bool] or bool)             : boolean if the fixations are global positioned or locally
                                                                            (in reference to the object itself)
            keepSizeFix         (tuple[bool, bool] or bool)             : boolean if the connection should keep size fixes or override them
        """
        body1idx: int = LayoutManager.getBodyIdx(body)
        body2: int | iRect
        if isinstance(fixTo, Body):
            body2 = LayoutManager.getBodyIdx(fixTo)
        else:
            body2 = fixTo
        if isinstance(keepSizeFix, bool):
            keepSizeFix = (keepSizeFix, keepSizeFix)
        if isinstance(fixedGlobal, bool):
            fixedGlobal = (fixedGlobal, fixedGlobal)

        newJoint: Joint = Joint(dimension=connectionDimension, start=(body1idx, bodyFixPoint), end=(body2, otherFixPoint), 
                                offset=offset, fixedGlobal=fixedGlobal, keepSizeFix=keepSizeFix)
        LayoutManager.__l_joints.append(newJoint)
        

    @staticmethod
    def applyLayout() -> None:
        """
        applyLayout updates the layout by applying the stored connections.
        """
        for joint in LayoutManager.__l_joints:
            dim: tuple[bool, bool] = joint.dimension
            start: tuple[int, Point] = joint.start
            end: tuple[int | iRect, Point] = joint.end
            startBody: Body = LayoutManager.__l_bodys[start[0]]

            endBody: iRect
            if isinstance(end[0], iRect):
                endBody = end[0]
            else:
                endBody = LayoutManager.__l_bodys[end[0]]

            startBody.applyConnection(endBody, dim, start[1], end[1], joint.offset, joint.fixedGlobal, joint.keepSizeFix)

    @staticmethod
    def forceApplyLayout() -> None:
        """
        forceApplyLayout applies the layout as many times as it takes to fully
        achieve all relation connections.
        """
        mybods: list[None | int] = [None for _ in range(len(LayoutManager.__l_bodys))]

        def calculateDepth(s: None | int) -> int:
            if s is None:
                return 0
            nonlocal mybods
            if mybods[s] is None or s < 0:
                return 0
            return 1 + calculateDepth(mybods[s])
        
        for j in LayoutManager.__l_joints:
            si: int = j.start[0]
            ee: int | iRect = j.end[0]
            if not isinstance(ee, int):
                ee = -1
            en: int = calculateDepth(ee)
            if calculateDepth(si) < en + 1:
                mybods[si] = ee

        neededit: int = max([calculateDepth(x) for x in range(len(mybods))])
        print("#Updates:",neededit)
        for _ in range(neededit):
            LayoutManager.applyLayout()


