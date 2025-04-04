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

    # ------------------------- line ------------------------
    l1: Line = Line(Rect((0, 0), (100, 100)), renderData=LinePrefab.DOTTED)
    l2: Line = Line(Rect((0, 0), (100, 100)), renderData=[LineCO.COLOR1, LineCO.DOTTED, LineCO.FLIPPED, LineCO.ALTLENGTH20])

    # ------------------------- box ------------------------
    ob1: Box = Box(Rect((0,0),(100,100)), renderData=BoxPrefab.BASIC)
    ob2: Box = Box(Rect((0,0),(100,100)), renderData=[BoxCO.FILL_COLOR2, BoxCO.ALTCHECKERBOARD, BoxCO.ALTLENGTH20])


    # ------------------------- text ------------------------
    txt1ci: CreateInfo = Text.fromPrefab(TextPrefab.DYNAMIC_BASIC)
    txt1: Text = txt1ci.createElement(Rect((0,0),(220,100)), content='Hello World!')
    #txt1: Text = Text(Rect((0,240),(220,100)), 'Hello World!', renderData=TextPrefab.DYNAMIC_BASIC)
    
    
    # ----------------------- composite-elements ----------------------
    txt2: Text = Text.fromPrefab(TextPrefab.DYNAMIC_BASIC).createElement(Rect((0,0),(165, 105)), content='WRAPPED :)')
    f1: Framed = Framed(txt2, renderData=[BoxCO.FILL_COLOR2, LineCO.COLOR1, FramedCO.USEBORDER_RB, LineCO.DOTTED, FramedCO.USEBORDER_R, LineCO.ALTLENGTH20])
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
    ob2.alignnextto(ob1, 3, offset=20)
    l1.alignaxis(ob2, 2)
    l2.alignaxis(ob2, 2)
    l1.alignnextto(ob2, 1, offset=20)
    l2.alignnextto(ob2, 1, offset=20)
    txt1.alignnextto(ob2, 3, offset=20)
    f1.alignnextto(txt1, 3, offset=20)

    movecallbackid: str = ''
    toggle: bool = True
    def moveLayout():
        nonlocal toggle, ob1, movecallbackid
        if toggle:
            ob1.alignaxis(Rect((0, 200),(0,0)), 2)
        else:
            ob1.alignaxis(Rect(), 2)
            EventManager.unsubscribeToEvent(InputManager.getEvent(InputEvent.M_DOWN), movecallbackid)
        LayoutManager.forceApplyLayout()
        toggle = not toggle
    
    movecallbackid: str = EventManager.createCallback(moveLayout)
    InputManager.subscribeToEvent(InputEvent.M_DOWN, movecallbackid)

    # ------------------------- render ------------------------
    LayoutManager.forceApplyLayout()

    while running:
        InputManager.update()

        main_screen.fill('black')
        Renderer.renderAll(PygameSurface(main_screen), [l1, l2, ob1, ob2, txt1, f1])#, btn1])#, btn2])

        pg.display.flip()

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()


