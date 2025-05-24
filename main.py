from time import perf_counter_ns
import pygame as pg

from pygamesetup import PygameDrawer, PygameSurface, PygameFont, PygameInputHandler

from ui import Rect, Parser, InputManager, InputEvent, Renderer

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
    def loadLayout(path: str | tuple[str, float, float]):
        sizing: tuple[float, float] = (0.5, 0.5)
        if isinstance(path, tuple):
            sizing = (path[1], path[2])
            path = path[0]
        layout = Parser.fromXML(path)
        layout.align(Rect(topleft=(int(screen_size[0]*(1.0-sizing[0])/2), int(screen_size[1]*(1.0-sizing[1])/2))))
        layout.alignSize(Rect(size=(int(screen_size[0]*sizing[0]), int(screen_size[1]*sizing[1]))))
        layout.updateLayout()
        return layout
    
    layouts = [loadLayout(pp) for pp in ['layouts/buttonexample.xml', ('layouts/dropdownexample.xml', 0.1, 0.1),'layouts/groupedexample.xml','layouts/framedexample.xml',
                                         ('layouts/boxexample.xml', 960/1280, 560/720),'layouts/boxexample2.xml',('layouts/lineexample.xml', 0.2, 0.2),'layouts/textexample.xml']]
    
    # ------------------------------ basic-functionality ------------------------------
    li, ln = 0, len(layouts)

    def switchUI():
        nonlocal li, ln
        li = (li + 1) % ln

    InputManager.quickSubscribe(InputEvent.M_DOWN, switchUI)

    def sayHi():
        print('Hi from button!')

    Parser.getElementByID('b1').set({'quickSubscribeToClick':(sayHi,[])})
    
    # ------------------------------ runtime-loop ------------------------------
    rt = 0
    fc = 0

    while running:
        InputManager.update()

        main_screen.fill(background_color)
        s = perf_counter_ns()
        layouts[li].renderAll(PygameSurface(main_screen), [layouts[li]])
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

