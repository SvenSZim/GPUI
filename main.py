from numpy import where
import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect
from ui import InputEvent, InputManager
from ui import UIRenderer, UIStyle
from ui import UILine, UISLine, UISObjectCreateOptions
from ui import UIObject, UISObject, UISObjectCreateOptions
from ui import UIText, UITextCore, UISText
from ui import UIButton, UIButtonCore, UISButton
from ui import UICTextCycleButton
from ui import UICreateInfo

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

    l1: UILine = UILine(Rect((120, 120), (100, 100)), renderStyleData=UISLine.DOTTED)
    l2: UILine = UILine(Rect((120, 220), (100, -100)))

    ob1: UIObject = UIObject(Rect((0,0),(100,100)), renderStyleData=UISObject.BORDER_SHRINKED_DOTTED)
    ob2: UIObject = UIObject(Rect((0,120),(100,100)), renderStyleData=[UISObjectCreateOptions.BORDER_COLOR2, UISObjectCreateOptions.BORDER_RIGHT,
                                                                       UISObjectCreateOptions.BORDER_BOTTOM])

    txt1ci: UICreateInfo = UICreateInfo(UIText, content='Hello World!', renderStyleData=UISText.DYNAMIC_BASIC)
    txt1: UIText = txt1ci.createElement(Rect((0,240),(220,100)))
    #txt1: UIText = UIText(UITextCore(Rect((0,240),(220,100)), 'Hello World!'), renderStyleData=UISText.DYNAMIC_BASIC)
    
    contents: list[str] = str('Hello World How Are U Doin Today').split()
    idx: int = 0
    def updateContentOfTxt1():
        nonlocal contents, txt1, idx
        txt1.updateContent(contents[idx])
        idx += 1
        idx %= len(contents)

    toggle: bool = True
    def updateContentOfTxt2():
        nonlocal txt1, toggle
        if toggle:
            txt1.updateContent('Cool')
        else:
            txt1.updateContent('Not Cool')
        toggle = not toggle

    btn1: UIButton = UIButton(UIButtonCore(Rect((0,360),(100,100)), numberOfStates=6, startState=2), renderStyleData=UISButton.BASIC_FILLING2)
    btn1.subscribeToButtonClick(updateContentOfTxt1)
    btn1.addGlobalButtonTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    #btn2: UICTextCycleButton = UICTextCycleButton(Rect((120, 0),(220,100)),['WOW', 'This', ('Actually', '1'), 'Works'])
    #btn2.subscribeToButtonEvent('1', updateContentOfTxt2)

    while running:
        InputManager.update()

        main_screen.fill('black')
        UIRenderer.renderAll(PygameSurface(main_screen), [l1, l2, ob1, ob2, txt1, btn1])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()


