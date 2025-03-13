

class Rect:

    top: int
    left: int
    bottom: int
    right: int

    width: int
    height: int

    def __init__(self, topleft: tuple[int, int], size: tuple[int, int]) -> None:
        self.left, self.top = topleft
        self.width, self.height = size
        self.right = self.left + self.width
        self.bottom = self.top + self.height
