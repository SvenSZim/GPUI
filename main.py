import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import InputEvent, InputManager
from ui import UIRenderer, UIStyle

from ui import UIDynamicBody
from ui import UIText, UIDynamicTextRenderer
from ui import UICycleButton, UICycleButtonRenderer


def setText(textobj: UIDynamicTextRenderer, newtext):
    textobj.updateContent(newtext)

def switchList(textobj: UIDynamicTextRenderer, l: list[str], i: int):
    textobj.updateContent(l[i])

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

    textbody1: UIDynamicBody = UIDynamicBody((50,50), (500, 200))
    text1_core: UIText = UIText(textbody1, 'Hello')
    text1: UIDynamicTextRenderer = UIDynamicTextRenderer(text1_core, 'Arial', 'white')
    
    textbody2 = UIDynamicBody((150,550), (700, 80))
    text2_core: UIText = UIText(textbody2, 'Hello')
    text2: UIDynamicTextRenderer = UIDynamicTextRenderer(text2_core, 'Arial', 'white')

    textbody = UIDynamicBody((0, 0), (200, 150), relativeObjectsForPosition=(textbody1, textbody2), relativeObjectsForPositionRelationType=(2,0))
    button_core: UICycleButton = UICycleButton(textbody, numberOfStates=8)
    button: UICycleButtonRenderer = UICycleButtonRenderer(button_core)
    button_core.addTriggerEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN))
    button_core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    [button_core.subscribeToButtonEvent(x, switchList, text1, ['Hello World!', 'My', 'name',  'is', 'sven!'], x) for x in range(5)]
    button_core.subscribeToButtonEvent(3, setText, text2, 'Moinsen from Button. YOLO ROFL XD :P')

    while running:
        InputManager.update()

        main_screen.fill('black')
        UIRenderer.render(PygameSurface(main_screen), [text1, text2, button])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()
