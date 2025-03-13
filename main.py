import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import InputEvent, InputManager
from ui import UIRenderer

from ui import UIDynamicBody
from ui import UIText, UIDynamicTextRenderInfo, UIDynamicTextRender
from ui import UICycleButton, UICycleButtonRenderInfo, UICycleButtonRender

def sayHello():
    print('HELLO')

def switchText(textobj: UIDynamicTextRender, newtext):
    textobj.getUIObject().setContent(newtext)
    textobj.update()

def switchList(textobj: UIDynamicTextRender, l: list[str]):
    l[0], l[1] = l[1], l[0]
    textobj.getUIObject().setContent(l[0])
    textobj.update()

def main():
    pg.init()
    pg.font.init()
    InputManager.init()
    renderer: UIRenderer = UIRenderer(PygameDrawer, PygameFont)
    
    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.subscribeToEvent(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)

    main_font: pg.font.Font = pg.font.SysFont('Arial', 10)

    textbody: UIDynamicBody = UIDynamicBody((50,50), (500, 200))
    text: UIDynamicTextRender = UIDynamicTextRender(UIText(textbody, 'Hello'), UIDynamicTextRenderInfo())
    textbody = UIDynamicBody((150,550), (700, 80))
    text2: UIDynamicTextRender = UIDynamicTextRender(UIText(textbody, 'Hello'), UIDynamicTextRenderInfo())

    textbody = UIDynamicBody((0, 0), (200, 150), relativeObjectsPosition=(text.getUIObject().body, text2.getUIObject().body), relativeObjectsPositionType=(2,2))
    button: UICycleButtonRender = UICycleButtonRender(UICycleButton(textbody, numberOfStates=5), UICycleButtonRenderInfo())
    button.getUIObject().addTriggerEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN))
    button.getUIObject().addGlobalTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    button.getUIObject().subscribeToButtonEvent(switchList, text, ['Hello World!', 'My name is sven'])
    button.getUIObject().subscribeToButtonEvent(switchText, text2, 'Moinsen from Button. YOLO ROFL XD :P')

    while running:
        InputManager.update()

        main_screen.fill('black')
        renderer.render(PygameSurface(main_screen), [text, text2, button])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()
