from time import perf_counter_ns
import pygame as pg

from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect, Parser, InputManager, InputEvent, Renderer, RenderStyle

def main():
    pg.init()
    pg.font.init()

    # ------------------------- setup ------------------------
    InputManager.init()
    Renderer.init(PygameDrawer, PygameFont, RenderStyle.MOON)

    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.quickSubscribe(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)
    background_color = 'black'
    
    def loadLayout(path):
        layout = Parser.fromXML(path)
        layout.align(Rect())
        layout.alignSize(Rect(size=screen_size))
        layout.updateLayout()
        return layout
    
    layouts = [loadLayout(pp) for pp in ['setup.xml','layouts/boxexample.xml','layouts/boxexample2.xml','layouts/lineexample.xml','layouts/textexample.xml']]
    li, ln = 0, len(layouts)

    def switchUI():
        nonlocal li, ln
        li = (li + 1) % ln

    InputManager.quickSubscribe(InputEvent.M_DOWN, switchUI)
    
    rt = 0
    fc = 0

    while running:
        InputManager.update()

        main_screen.fill(background_color)
        s = perf_counter_ns()
        layouts[li].render(PygameSurface(main_screen))
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

