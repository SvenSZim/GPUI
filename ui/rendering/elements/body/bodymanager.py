
from .body import Body
from .layoutmanager import LayoutManager

class BodyManager:
    """
    BodyManager is a simple 'static' class to use for creating Body objects.
    Its important to use the BodyManager for creating Body's because they need
    to be registered in the LayoutManager.
    """

    @staticmethod
    def createBody() -> Body:
        """
        createBody is the function to use when creating Body objects.

        Returns (Body): the newly created Body object
        """
        body: Body = Body()
        LayoutManager.addBody(body) # registers the new Body object in LayoutManager
        return body
