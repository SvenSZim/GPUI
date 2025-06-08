from time import perf_counter_ns
import pygame as pg

from pygamesetup import PygameDrawer, PygameSurface, PygameFont, PygameInputHandler

from ui import Parser, InputManager, InputEvent, UI

def main():
    pg.init()
    pg.font.init()

    # ------------------------------ setup ------------------------------
    InputManager.init(PygameInputHandler)
    UI.init(PygameDrawer, PygameFont)

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
    ui: UI = Parser.loadLayoutFromXML("layoutexample.xml")
    ui.setSize(screen_size)
    ui.setActive(True)

    txt = ui.getElementByID('imp')
    txt.set({'content':'UNIMPORTANT'})

    print(Parser.getAllStyles())

    # ------------------------------ runtime-loop ------------------------------
    rt = 0
    fc = 0

    while running:
        InputManager.update()

        main_screen.fill(background_color)
        s = perf_counter_ns()
        ui.render(PygameSurface(main_screen))
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

