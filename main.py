import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect
from ui import InputEvent, InputManager
from ui import Renderer, RenderStyle
from ui import CreateInfo
from ui import LayoutManager
from ui import Line, LinePrefab, LineCO
from ui import Box, BoxPrefab, BoxCO
#from ui import Text, TextPrefab, TextCO
#from ui import Button, ButtonPrefab, ButtonCO
#from ui import TextCycleButton

def main():
    pg.init()
    pg.font.init()
    InputManager.init()
    Renderer.init(PygameDrawer, PygameFont, RenderStyle.MOON)

    running: bool = True

    def quit():
        nonlocal running
        running = False

    InputManager.subscribeToEvent(InputEvent.QUIT, quit)
    
    screen_size = (1280, 720)
    main_screen = pg.display.set_mode(screen_size)

    l1: Line = Line(Rect((120, 120), (100, 100)), renderStyleData=LinePrefab.DOTTED)
    l2: Line = Line(Rect((120, 120), (100, 100)), renderStyleData=[LineCO.COLOR1, LineCO.DOTTED, LineCO.FLIPPED, LineCO.ALTLENGTH20])

    ob1: Box = Box(Rect((0,0),(100,100)), renderStyleData=BoxPrefab.BORDER_SHRINKED_DOTTED)
    ob2: Box = Box(Rect((0,120),(100,100)), renderStyleData=[BoxCO.BORDER_COLOR2, BoxCO.BORDER_RIGHT,
                                                                      BoxCO.BORDER_BOTTOM])

    #txt1ci: UICreateInfo = UICreateInfo(UIText, content='Hello World!', renderStyleData=UISText.DYNAMIC_BASIC)
    #txt1: UIText = txt1ci.createElement(Rect((0,240),(220,100)))
    #txt1: UIText = UIText(UITextCore(Rect((0,240),(220,100)), 'Hello World!'), renderStyleData=UISText.DYNAMIC_BASIC)
    
    #contents: list[str] = str('Hello World How Are U Doin Today').split()
    #idx: int = 0
    #def updateContentOfTxt1():
    #   nonlocal contents, txt1, idx
    #   txt1.updateContent(contents[idx])
    #   idx += 1
    #   idx %= len(contents)

    #toggle: bool = True
    #def updateContentOfTxt2():
    #   nonlocal txt1, toggle, ob1
    #   if toggle:
    #       txt1.updateContent('Cool')
    #       ob1.setRect(Rect((0,0), (150, 100)))
    #   else:
    #       txt1.updateContent('Not Cool')
    #       ob1.setRect(Rect((0,0), (100, 100)))
    #   toggle = not toggle

    #btn1: UIButton = UIButton(UIButtonCore(Rect((0,360),(100,100)), numberOfStates=6, startState=2), renderStyleData=UISButton.BASIC_FILLING2)
    #btn1.subscribeToButtonClick(updateContentOfTxt1)
    #btn1.addGlobalButtonTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    #db: UIDynamicBody = UIDynamicBody((20, 0), (220, 100), relativeObjectsForPosition=(ob1, ob1), relativeObjectsForPositionRelationType=(0, 1))
    #btn2: UICTextCycleButton = UICTextCycleButton.constructor(db,['WOW', 'This', ('Actually', '1'), 'Works'])
    #btn2.subscribeToButtonEvent('1', updateContentOfTxt2)
    #btn2.subscribeToButtonEvent('1', UIRenderer.updateAll)

    while running:
        InputManager.update()

        main_screen.fill('black')
        Renderer.renderAll(PygameSurface(main_screen), [l1, l2, ob1, ob2])#, txt1, btn1, btn2])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()


