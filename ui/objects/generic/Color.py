

class Color:

    value: tuple[int, int, int]

    def __init__(self, value: tuple[int, int, int] | str) -> None:
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
                    raise ValueError("Color::__init__::value")
        else:
            self.value = value
