import pygame as pg

from ui import InputEvent, InputManager
from ui import UIObjectBody, UIText, UIDynamicText, UIButton
from ui import UIRenderer
from ui import DynamicCycleState
from ui import ButtonRenderStyle

def sayHello():
    print('HELLO')

def switchText(textobj: UIText, newtext):
    textobj.updateContent(newtext)

def switchList(textobj: UIText, l: list[str]):
    l[0], l[1] = l[1], l[0]
    textobj.updateContent(l[0])

def main():
    pg.init()
    pg.font.init()
    InputManager.init()
    renderer: UIRenderer = UIRenderer(buttonrenderstyle=ButtonRenderStyle.FILLING_DIAGONALALT)
    
    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.subscribeToEvent(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)

    main_font: pg.font.Font = pg.font.SysFont('Arial', 10)

    textbody: UIObjectBody = UIObjectBody((50,50), (500, 200))
    text: UIDynamicText = UIDynamicText(textbody, 'Hello', 'Arial', 'white')
    textbody = UIObjectBody((150,550), (700, 80))
    text2: UIDynamicText = UIDynamicText(textbody, 'Hello', 'Arial', 'white')

    textbody = UIObjectBody((0, 0), (200, 150), relativeObjectsPosition=(text, text2), relativeObjectsPositionType=(2,2))
    button: UIButton = UIButton(textbody, DynamicCycleState(0, 5))
    button.addTriggerEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONDOWN))
    button.addGlobalResetEvent(InputManager.getEvent(InputEvent.MOUSEBUTTONUP))
    button.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    button.subscribeToButtonEvent(switchList, text, ['Hello World!', 'My name is sven'])
    button.subscribeToButtonEvent(switchText, text2, 'Moinsen from Button. YOLO ROFL XD :P')

    while running:
        InputManager.update()

        main_screen.fill('black')
        renderer.render(main_screen, [text, text2, button])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()
