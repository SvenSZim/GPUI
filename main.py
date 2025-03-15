import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect
from ui import InputEvent, InputManager
from ui import UIRenderer, UIStyleMOON

from ui import UIDynamicBody, UIStaticBody
from ui import UIText, UIFont, UIDynamicTextRenderer
from ui import UICycleButton, UICycleButtonRenderer
from ui.objects.uiobject.UIObject import UIObjectRenderer
from ui.objects.uitext.UIStaticText import UIStaticTextRenderer


def setText(textobj: UIDynamicTextRenderer, newtext):
    textobj.updateContent(newtext)

def switchList(textobj: UIDynamicTextRenderer, l: list[str], i: int):
    textobj.updateContent(l[i])

def main():
    pg.init()
    pg.font.init()
    InputManager.init()
    UIRenderer.init(PygameDrawer, PygameFont, UIStyleMOON)

    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.subscribeToEvent(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)

    main_font: UIFont = PygameFont(pg.font.SysFont('Arial', 24))

    obj1: UIObjectRenderer = UIObjectRenderer(Rect((600, 0), (100, 200)))

    text1_core: UIText = UIText(Rect((50,50), (500, 200)), 'Hello')
    text1: UIDynamicTextRenderer = UIDynamicTextRenderer(text1_core, 'Arial', 'white')
    
    text2_core: UIText = UIText(Rect((150,550), (700, 80)), 'Hello')
    text2: UIStaticTextRenderer = UIStaticTextRenderer(text2_core, main_font, 'white')

    textbody = UIDynamicBody((10, -1.0), (200, 150), relativeObjectsForPosition=(text1_core.getBody(), text2_core.getBody()), relativeObjectsForPositionRelationType=(3,1))
    button_core: UICycleButton = UICycleButton(textbody, numberOfStates=2)
    button: UICycleButtonRenderer = UICycleButtonRenderer(button_core)
    button_core.addTriggerEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN))
    button_core.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    [button_core.subscribeToButtonEvent(x, switchList, text1, ['Hello', 'World', 'My', 'name',  'is', 'sven!'], x) for x in range(5)]
    button_core.subscribeToButtonEvent(3, setText, text2, 'Moinsen from Button. YOLO ROFL XD :P')

    while running:
        InputManager.update()

        main_screen.fill('black')
        UIRenderer.render(PygameSurface(main_screen), [obj1, text1, text2, button])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()
