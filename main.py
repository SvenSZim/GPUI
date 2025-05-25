import os, json
from time import perf_counter_ns
import pygame as pg

from pygamesetup import PygameDrawer, PygameSurface, PygameFont, PygameInputHandler

from ui import Rect, Parser, InputManager, InputEvent, Renderer

layout_paths: list[tuple[str, float]] = []
filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.json')
with open(filepath,'r') as file:
    layout_paths = [(p, v) for p, v in json.load(file).items()]

def main():
    pg.init()
    pg.font.init()

    # ------------------------------ setup ------------------------------
    InputManager.init(PygameInputHandler)
    Renderer.init(PygameDrawer, PygameFont)

    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.quickSubscribe(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)
    background_color = 'black'
    
    # ------------------------------ load-layouts ------------------------------
    def loadLayout(path: tuple[str, float]):
        sizing: tuple[float, float] = (path[1], path[1])
        layout = Parser.fromXML(path[0])
        layout.align(Rect(topleft=(int(screen_size[0]*(1.0-sizing[0])/2), int(screen_size[1]*(1.0-sizing[1])/2))))
        layout.alignSize(Rect(size=(int(screen_size[0]*sizing[0]), int(screen_size[1]*sizing[1]))))
        layout.updateLayout()
        layout.setActive(False)
        return layout
    
    layout = loadLayout(layout_paths[0])
    layout.setActive(True)

    # ------------------------------ runtime-loop ------------------------------
    rt = 0
    fc = 0

    while running:
        InputManager.update()

        main_screen.fill(background_color)
        s = perf_counter_ns()
        layout.renderAll(PygameSurface(main_screen), [layout])
        rt += perf_counter_ns() - s
        fc += 1

        #if fc > 1000:
        #    print(f'Avg rendertime: {rt/fc/1000}')

        pg.display.flip()
        background_color = 'black'

    print(f'Avg rendertime: {rt/fc/1000}')
    

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()

