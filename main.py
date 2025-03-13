import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import InputEvent, InputManager
from ui import UIRenderer, UIStyle

from ui import UIDynamicBody
from ui import UIText, UIDynamicTextRenderer
from ui import UICycleButton, UICycleButtonRenderer


def setText(textobj: UIDynamicTextRenderer, newtext):
    textobj.getUIObject().setContent(newtext)
    textobj.update()

def switchList(textobj: UIDynamicTextRenderer, l: list[str], i: int):
    textobj.getUIObject().setContent(l[i])
    textobj.update()

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

    main_font: pg.font.Font = pg.font.SysFont('Arial', 10)

    textbody: UIDynamicBody = UIDynamicBody((50,50), (500, 200))
    text: UIDynamicTextRender = UIDynamicTextRenderer(UIText(textbody, 'Hello'))
    
    textbody = UIDynamicBody((150,550), (700, 80))
    text2: UIDynamicTextRender = UIDynamicTextRenderer(UIText(textbody, 'Hello'))

    textbody = UIDynamicBody((0, 0), (200, 150), relativeObjectsPosition=(text.getUIObject().body, text2.getUIObject().body), relativeObjectsPositionType=(2,0))
    button: UICycleButtonRender = UICycleButtonRenderer(UICycleButton(textbody, numberOfStates=8))
    button.getUIObject().addTriggerEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN))
    button.getUIObject().addGlobalTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    [button.getUIObject().subscribeToButtonEvent(x, switchList, text, ['Hello World!', 'My', 'name',  'is', 'sven!'], x) for x in range(5)]
    button.getUIObject().subscribeToButtonEvent(3, setText, text2, 'Moinsen from Button. YOLO ROFL XD :P')

    while running:
        InputManager.update()

        main_screen.fill('black')
        UIRenderer.render(PygameSurface(main_screen), [text, text2, button])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()
