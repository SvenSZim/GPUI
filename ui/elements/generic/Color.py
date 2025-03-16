from typing import Union

class tColor:
    """
    Color is a utility class for defining and storing color related data
    """

    value: tuple[int, int, int] # rgb color value

    def __init__(self, value: tuple[int, int, int] | str) -> None:
        """
        __init__ initializes a Color object

        Args:
            value: tuple[int, int, int] | str = rgb value of color or a color as string
        """
        if isinstance(value, str):
            match value:
                case 'white':
                    self.value = (255, 255, 255)
                case 'black':
                    self.value = (0, 0, 0)
                case 'red':
                    self.value = (255, 0, 0)
                case 'green':
                    self.value = (0, 255, 0)
                case 'blue':
                    self.value = (0, 0, 255)
                case _:
                    raise ValueError(f'Color::__init__::{value=}')
        else:
            self.value = value


Color = Union[str, tuple[int, int, int], tColor]
