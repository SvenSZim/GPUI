import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect
from ui import InputEvent, InputManager
from ui import UIRenderer, UIStyle
from ui import UILine, UISLine, UISLineCreateOptions
from ui import UIObject, UISObject, UISObjectCreateOptions
from ui import UIText, UITextCore, UISText, UISTextCreateOptions


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

    l1: UILine = UILine(Rect((120, 120), (100, 100)))
    l2: UILine = UILine(Rect((120, 220), (100, -100)))

    ob1: UIObject = UIObject(Rect((0,0),(100,100)), renderStyleData=UISObject.BASIC)
    ob2: UIObject = UIObject(Rect((0,120),(100,100)), renderStyleData=[UISObjectCreateOptions.BORDER_COLOR1, UISObjectCreateOptions.BORDER_RIGHT,
                                                                       UISObjectCreateOptions.BORDER_BOTTOM])

    txt1_core: UITextCore = UITextCore(Rect((0,240),(220,100)), 'Hello World!')
    txt1: UIText = UIText(txt1_core, renderStyleData=UISText.BASIC)

    txt1_core.setContent('I was here.')

    while running:
        InputManager.update()

        main_screen.fill('black')
        UIRenderer.renderAll(PygameSurface(main_screen), [l1, l2, ob1, ob2, txt1])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()


