from time import perf_counter_ns
import pygame as pg

from pygamesetup import PygameDrawer, PygameSurface, PygameFont, PygameInputHandler

from ui import Rect, Parser, InputManager, InputEvent, Element, StyleManager

def main():
    pg.init()
    pg.font.init()

    # ------------------------------ setup ------------------------------
    InputManager.init(PygameInputHandler)
    Element.init(PygameDrawer, PygameFont)

    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.quickSubscribe(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)
    background_color = 'black'
    
    # ------------------------------ load-layouts ------------------------------
 
    Parser.loadStyleFromXML("styleexample.xml")
    Parser.setDefaultStyle('moon')
    layout = Parser.loadLayoutFromXML("layoutexample.xml")
    relSize = (0.7, 0.7)
    layout.align(Rect(topleft=(int(screen_size[0]*(1-relSize[0])*0.5),int(screen_size[1]*(1-relSize[1])*0.5))))
    layout.alignSize(Rect(size=(int(screen_size[0]*relSize[0]),int(screen_size[1]*relSize[1]))))
    layout.updateLayout()
    layout.setActive(True)

    txt = Parser.getElementByID('imp')
    txt.set({'content':'UNIMPORTANT'})

    print(Parser.getAllStyles())

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

