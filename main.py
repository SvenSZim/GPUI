import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect, Parser, InputManager, InputEvent, Renderer, RenderStyle, Element

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

    ui: Element = Parser.fromXML('setup.xml')
    ui.alignSize(Rect(size=screen_size))
    ui.updateLayout()
    
    while running:
        InputManager.update()

        main_screen.fill(background_color)
        ui.render(PygameSurface(main_screen))

        pg.display.flip()
        background_color = 'black'

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()

