import pygame as pg
from drawer import PygameDrawer, PygameSurface, PygameFont

from ui import Rect
from ui import InputEvent, InputManager, EventManager
from ui import Renderer, RenderStyle
from ui import CreateInfo
from ui import LayoutManager
from ui import Line, LinePrefab, LineCO
from ui import Box, BoxPrefab, BoxCO
from ui import Text, TextPrefab, TextCO

from ui import Framed, FramedCO, FramedPrefab
from ui import Button, ButtonCO, ButtonPrefab
from ui import Checkbox, CheckboxCO, CheckboxPrefab
#from ui import BoxCycleToggle
#from ui import TextCycleToggle

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

    # ------------------------- line ------------------------
    l1: Line = Line(Rect((0, 0), (100, 100)), renderData=LinePrefab.DOTTED)
    l2: Line = Line(Rect((0, 0), (100, 100)), renderData=[LineCO.COLOR1, LineCO.DOTTED, LineCO.FLIPPED, LineCO.ALTLENGTH20])

    # ------------------------- box ------------------------
    ob1: Box = Box(Rect((0,0),(100,100)), renderData=BoxPrefab.BASIC)
    ob2: Box = Box(Rect((0,0),(100,100)), renderData=[BoxCO.COLOR2, BoxCO.ALTCHECKERBOARD, BoxCO.ALTLENGTH20])


    # ------------------------- text ------------------------
    txt1ci: CreateInfo = Text.fromPrefab(TextPrefab.DYNAMIC_BASIC)
    txt1: Text = txt1ci.createElement(Rect((0,0),(220,100)), content='Hello World!')
    #txt1: Text = Text(Rect((0,240),(220,100)), 'Hello World!', renderData=TextPrefab.DYNAMIC_BASIC)
    
    
    # ----------------------- composite-elements ----------------------
    txt2: Text = Text.fromPrefab(TextPrefab.DYNAMIC_BASIC).createElement(Rect((0,0),(152, 92)), content='WRAPPED :)')
    f1: Framed = Framed(txt2, offset=8, renderData=[BoxCO.COLOR2, LineCO.COLOR1, FramedCO.USEBORDER_RB, LineCO.DOTTED, FramedCO.USEBORDER_R, LineCO.ALTLENGTH20])

    b1: Button = Button(Rect((0,0),(100,100)), renderData=[BoxCO.COLOR2, BoxCO.PARTIAL_80])
    f2: Framed = Framed(b1, renderData=[LineCO.COLOR1])

    cb1: Checkbox = Checkbox(Rect((0,0),(100,100)), renderData=[CheckboxCO.USECROSS, LineCO.COLOR1])
    f3: Framed = Framed(cb1, renderData=[LineCO.COLOR1])
    #contents: list[str] = str('Hello World How Are U Doin Today').split()
    #idx: int = 0
    #def updateContentOfTxt1():
    #   nonlocal contents, txt1, idx
    #   txt1.updateContent(contents[idx])
    #   idx += 1
    #   idx %= len(contents)


    #btn1: Toggle = Toggle(Rect((0,0),(100, 230)), numberOfStates=6, startState=2, renderData=TogglePrefab.BASIC_ALT)
    #btn1.subscribeToClick(updateContentOfTxt1)
    #btn1.subscribeToToggleState(3, moveLayout)
    #btn1.addGlobalTriggerEvent(InputManager.getEvent(InputEvent.A_DOWN))

    #btn1.alignnextto(txt1, 3, offset=20)

    #db: UIDynamicBody = UIDynamicBody((20, 0), (220, 100), relativeObjectsForPosition=(ob1, ob1), relativeObjectsForPositionRelationType=(0, 1))
    #btn2: UICTextCycleToggle = UICTextCycleToggle.constructor(db,['WOW', 'This', ('Actually', '1'), 'Works'])
    #btn2.subscribeToToggleEvent('1', updateContentOfTxt2)
    #btn2.subscribeToToggleEvent('1', UIRenderer.updateAll)


    # ------------------------- layout ------------------------
    ob2.alignpoint(ob1, (0,0),(0,1), offset=(0,20))
    l1.alignpoint(ob2, (0,0),(1,0), offset=(20,0))
    l2.alignpoint(ob2, (0,0),(1,0), offset=(20,0))
    txt1.alignpoint(ob2, (0,0),(0,1), offset=(0,20))
    f1.alignpoint(txt1, (0,0),(0,1), offset=(0,20))
    f2.alignpoint(ob1, (0,0),(1,0), offset=(20,0))
    f3.alignpoint(f2, (0,0),(1,0), offset=(20,0))

    movecallbackid: str = ''
    toggle: bool = True
    def moveLayout():
        nonlocal toggle, ob1, movecallbackid
        if toggle:
            ob1.alignpoint(Rect((200, 200),(0,0)))
        else:
            ob1.alignpoint(Rect())
            EventManager.unsubscribeToEvent(InputManager.getEvent(InputEvent.M_DOWN), movecallbackid)
        LayoutManager.forceApplyLayout()
        toggle = not toggle
    
    movecallbackid: str = EventManager.createCallback(moveLayout)
    InputManager.subscribeToEvent(InputEvent.M_DOWN, movecallbackid)

    # ------------------------- action ------------------------

    def flashbang():
        nonlocal background_color
        background_color = 'darkred'

    b1.quickSubscribeToHold(flashbang)

    def moveRight():
        nonlocal ob1
        ob1.alignaxis(Rect(), 0, offset=200)
        LayoutManager.forceApplyLayout()

    def moveLeft():
        nonlocal ob1
        ob1.alignaxis(Rect(), 0)
        LayoutManager.forceApplyLayout()

    cb1.quickSubscribeToSelect(moveRight)
    cb1.quickSubscribeToDeselect(moveLeft)

    # ------------------------- render ------------------------
    LayoutManager.forceApplyLayout()

    while running:
        InputManager.update()

        main_screen.fill(background_color)
        Renderer.renderAll(PygameSurface(main_screen), [l1, l2, ob1, ob2, txt1, f1, f2, f3])#, btn1])#, btn2])

        pg.display.flip()
        background_color = 'black'

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()


