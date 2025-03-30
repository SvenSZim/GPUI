    @override
    def render(self, surfaceDrawer: type[UISurfaceDrawer], surface: UISurface) -> None:
        """
        render renders the UIObject onto the given surface

        Args:
            surface: UISurface = the surface the UIObject should be drawn on
        """

        # check if UIElement should be rendered
        if not self._active:
            return


        surfaceDrawer.drawrect(surface, self._core.getRect(), 'white', fill=False)

        color: str = 'white'

        rect: Rect = self._core.getRect()

        def fill_with_lines(screen: UISurface, rect: Rect,
                            line_function: Callable[[int], int], line_spacing: float, draw: bool = True) -> tuple[tuple[int, int], tuple[int, int]]:
            """
            Returns:
                tuple[
                    tuple[int, int],
                    tuple[int, int]
                ]: start_point and end_point of first drawn line
            """

            def find_y_intersect(f: Callable[[int], int], y: int) -> int:
                iterations: int = 10
                cx: int = 0
                while iterations > 0:
                    cy: int = f(cx)
                    cya: int = f(cx + 1)
                    if cy == cya:
                        cx += 1
                    else:
                        cx += (y - f(cx)) // (f(cx+1) - f(cx))
                    iterations -= 1
                return cx

            first_start_point: tuple[int, int] = (-1, -1)
            first_end_point: tuple[int, int] = (-1, -1)

            actual_line_amount: int = int((rect.height + rect.width)/line_spacing) #-1 ?
            for line_number in range(-actual_line_amount, actual_line_amount + 1):
                cline_f: Callable[[int], int] = lambda x: line_function(x - rect.left) + int(rect.top + line_number * line_spacing)

                # calculate start point
                start_pointX: int
                start_pointY: int = int(rect.top + line_number * line_spacing)
                if start_pointY < rect.top:
                    start_pointX = find_y_intersect(cline_f, rect.top)
                elif start_pointY > rect.bottom:
                    start_pointX = find_y_intersect(cline_f, rect.bottom)
                else:
                    start_pointX = rect.left
                start_point: tuple[int, int] = (start_pointX, cline_f(start_pointX))

                # calculate end point
                end_pointX: int = rect.right
                end_pointY: int = cline_f(end_pointX)
                if end_pointY < rect.top:
                    end_pointX = find_y_intersect(cline_f, rect.top)
                elif end_pointY > rect.bottom:
                    end_pointX = find_y_intersect(cline_f, rect.bottom)
                else:
                    end_pointX = rect.right
                end_point: tuple[int, int] = (end_pointX, cline_f(end_pointX))

                if start_pointX >= rect.left and end_pointX <= rect.right and start_pointX < end_pointX:
                    nonlocal color
                    
                    if draw:
                        surfaceDrawer.drawline(screen, start_point, end_point, color)

                    if first_start_point[0] == -1:
                        first_start_point = start_point
                        first_end_point = end_point

            return (first_start_point, first_end_point)

            
        line_amount: int = min(10, int(rect.height / 10))
        line_spacing: float = rect.height / (line_amount + 1)
        
        style: CycleButtonRenderStyle = CycleButtonRenderStyle.FILLING_DIAGONAL
        match style:
            case CycleButtonRenderStyle.DEFAULT:
                pass

            case CycleButtonRenderStyle.PLAIN:
                pass

            case CycleButtonRenderStyle.FILLING_HORIZONTAL:
                activation_percent: float = self._core.getCurrentState() / (self._core.getNumberOfStates() - 1)
                activation_width: int = int(rect.width * activation_percent)
                fill_with_lines(surface, Rect(rect.getPosition(), (activation_width, rect.height)), lambda x: x, line_spacing)
                fill_with_lines(surface, Rect(rect.getPosition(), (activation_width, rect.height)), lambda x: -x, line_spacing)

            case CycleButtonRenderStyle.FILLING_DIAGONAL:
                activation_percent: float = self._core.getCurrentState() / (self._core.getNumberOfStates() - 1)
                activation_width: int = int(rect.width * activation_percent)
                fill_with_lines(surface, Rect(rect.getPosition(), (activation_width, rect.height)), lambda x: x, line_spacing)

            case CycleButtonRenderStyle.FILLING_DIAGONALALT:
                state_percent: float = 1 / (self._core.getNumberOfStates() - 1)
                state_width: int = int(rect.width * state_percent)

                sign: bool = True
                # vertical offset to align the diagonal lines vertically
                p_end_point: tuple[int, int] = fill_with_lines(surface, Rect((0, rect.top), (state_width, rect.height)), lambda x: x, line_spacing, draw=False)[1]
                p_start_point: tuple[int, int] = fill_with_lines(surface, Rect((0, rect.top), (state_width, rect.height)), lambda x: -x, line_spacing, draw=False)[0]
                vertical_offset: int = p_end_point[1] - p_start_point[1]

                for cs in range(1, self._core.getCurrentState() + 1):
                    state_left: int = rect.left + (cs - 1) * state_width
                    if sign:
                        fill_with_lines(surface, Rect((state_left, rect.top), (state_width, rect.height)), lambda x: x, line_spacing)
                    else:
                        fill_with_lines(surface, Rect((state_left, rect.top), (state_width, rect.height)), lambda x: -x + vertical_offset, line_spacing)
                    sign = not sign
