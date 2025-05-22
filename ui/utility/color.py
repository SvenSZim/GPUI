import os, json
from typing import Union

class tColor:
    """
    Color is a utility class for defining and storing color related data
    """
    colornames: dict[str, str]={}

    @staticmethod
    def convert_strhex_to_rgb(x: str) -> tuple[int, int, int]:
        x_hex: int = int(x, 16)
        return ((x_hex & 0xff0000) >> 16, (x_hex & 0x00ff00) >> 8, (x_hex & 0x0000ff))

    @staticmethod
    def is_valid_color(x: str) -> bool:
        return x in tColor.colornames

    value: tuple[int, int, int] # rgb color value

    def __init__(self, value: tuple[int, int, int] | str) -> None:
        """
        __init__ initializes a Color object

        Args:
            value (tuple[int, int, int] or str): rgb value of color or a color as string
        """
        if isinstance(value, str):
            if tColor.is_valid_color(value):
                self.value = tColor.convert_strhex_to_rgb(tColor.colornames[value])
            else:
                raise ValueError(f'Invalid color name: {value}')
        else:
            self.value = value

filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colors.json')
with open(filepath,'r') as file:
    tColor.colornames = json.load(file)


Color = Union[str, tuple[int, int, int], tColor]
