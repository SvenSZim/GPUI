import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect
from ui import InputEvent, InputManager
from ui import UIRenderer, UIStyle
from ui import UIObject


def main():
    pg.init()
    pg.font.init()
    InputManager.init()
    UIRenderer.init(PygameDrawer, PygameFont, UIStyle.MOON)

    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.subscribeToEvent(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)

    ob1: UIObject = UIObject(Rect((0,0),(100,100)))

    while running:
        InputManager.update()

        main_screen.fill('black')
        UIRenderer.renderAll(PygameSurface(main_screen), [ob1])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()


