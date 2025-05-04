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

from ui import Framed, FramedCO, Stacked, Grouped, Section
from ui import Dropdown
from ui import Button, ButtonCO
from ui import Checkbox, CheckboxCO
from ui import Slider, SliderCO
from ui import TextCycle

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
    l1: Line = Line(Rect(size=(100, 100)), renderData=LinePrefab.DOTTED)
    l2: Line = Line(Rect(size=(100, 100)), renderData=[LineCO.COLOR1, LineCO.DOTTED, LineCO.FLIPPED, LineCO.ALTLENGTH20])

    # ------------------------- box ------------------------
    ob1: Box = Box(Rect((20,20),(100,100)), renderData=BoxPrefab.BASIC)
    ob2: Box = Box(Rect(size=(100,100)), renderData=[BoxCO.COLOR2, BoxCO.ALTCHECKERBOARD, BoxCO.ALTLENGTH20])


    # ------------------------- text ------------------------
    txt1ci: CreateInfo = Text.fromPrefab(TextPrefab.DYNAMIC_BASIC)
    txt1: Text = txt1ci.createElement(Rect(size=(220,100)), content='Hello World!')
    #txt1: Text = Text(Rect((0,240),(220,100)), 'Hello World!', renderData=TextPrefab.DYNAMIC_BASIC)
    
    
    # ----------------------- composite-elements ----------------------
    txt2: Text = Text.fromCreateOptions([TextCO.SIZE_SM ,TextCO.COLOR1, TextCO.ALIGNTOP]).createElement(Rect(size=(144, 84)), content='WRAPPED :)')
    f1: Framed = Framed(txt2, offset=0, renderData=[BoxCO.COLOR2, LineCO.COLOR1, FramedCO.USEBORDER_RB, LineCO.DOTTED, FramedCO.USEBORDER_R, LineCO.ALTLENGTH20])

    b1: Button = Button(Rect(size=(100,100)), renderData=[BoxCO.COLOR2, BoxCO.PARTIAL_80])
    f2: Framed = Framed(b1, renderData=[LineCO.COLOR1])

    cb1: Checkbox = Checkbox(Rect(size=(100,100)), renderData=[CheckboxCO.USECROSS, LineCO.COLOR1])
    f3: Framed = Framed(cb1, renderData=[LineCO.COLOR1])

    g1: Grouped = Grouped(Rect(size=(340, 90)), ob1, (f2, 0.2), (f3, 0.5), alignVertical=False, offset=20)
    f4: Framed = Framed(g1, offset=5, renderData=[LineCO.COLOR1, FramedCO.USEBORDER_LR, LineCO.DOTTED])
    
    s1: Slider = Slider(Rect(size=(440,80)), renderData=[BoxCO.COLOR1])
    f5: Framed = Framed(s1, offset=10, renderData=[LineCO.COLOR1])

    tc1: TextCycle = TextCycle(Rect(size=(200, 80)), contents=str("State1 State2 State3 State4 STATEABCDEFGHIJKL").split(),
                               renderData=[TextCO.COLOR1, TextCO.SIZEDYNAMIC])
    f6: Framed = Framed(tc1, offset=10, renderData=[LineCO.COLOR1])

    texts: list[Framed] = [Framed(Text.fromCreateOptions([TextCO.SIZE_M, TextCO.COLOR1]).createElement(Rect(), content=str(txt)),
                                  offset=10, renderData=[LineCO.COLOR1]) for txt in range(5)]
    stk1: Stacked = Stacked(Rect(), Rect(size=(90, 50)), texts[0], (texts[1], 2), (texts[2], 0.3), *texts[3:], offset=5)
    f8: Framed = Framed(stk1, offset=5, renderData=[LineCO.COLOR2, BoxCO.ALTCHECKERBOARD, BoxCO.COLOR2])
    
    f7: Framed = Framed(Text(Rect(size=(150, 80)), content="SELECT", renderData=[TextCO.COLOR1]), renderData=[BoxCO.COLOR2])
    texts2: list[Framed] = [Framed(Text.fromCreateOptions([TextCO.SIZE_M, TextCO.COLOR1]).createElement(Rect(), content=str(txt)),
                                  offset=10, renderData=[LineCO.COLOR1, BoxCO.COLOR2]) for txt in range(5)]
    dpd: Dropdown = Dropdown(f7, (texts2[0], 0.4), (texts2[1], 1.2), *texts2[2:], offset=10)

    texts3: list[Framed] = [Framed(Text.fromCreateOptions([TextCO.SIZE_M, TextCO.COLOR1]).createElement(Rect(), content=str(txt)),
                                  offset=10, renderData=[LineCO.COLOR1]) for txt in range(3, 8)]
    stk2: Stacked = Stacked(Rect(), Rect(size=(90, 50)), (texts3[0], 2.4), *texts3[1:-3], (texts3[-3], 1.5), offset=5)
    sec1: Section = Section(stk2, texts3[-2], texts3[-1], offset=50, renderData=[LineCO.COLOR1, LineCO.PARTIAL_70])

    # ------------------------- layout ------------------------
    f4.alignpoint(Rect(), offset=20)
    ob2.alignpoint(g1, otherPoint=(0,1), offset=(0,20))
    l1.alignpoint(ob2, otherPoint=(1,0), offset=(20,0))
    l2.alignpoint(ob2, otherPoint=(1,0), offset=(20,0))
    txt1.alignpoint(ob2, otherPoint=(0,1), offset=(0,20))
    f1.alignpoint(txt1, otherPoint=(0,1), offset=(0,20))
    f5.alignpoint(f1, otherPoint=(1,0), offset=(20,0))
    f6.alignpoint(l2, otherPoint=(1,0), offset=(20,0))
    f8.alignaxis(f4, 2)
    f8.alignnextto(f6, 1, offset=20)
    dpd.alignaxis(f8, 2)
    dpd.alignnextto(f8, 1, offset=20)
    sec1.alignaxis(dpd, 2)
    sec1.alignnextto(dpd, 1, offset=20)

    LayoutManager.applyLayout()
    # ------------------------- action ------------------------

    def flashbang():
        nonlocal background_color
        background_color = 'darkred'
    
    def getSliderValue():
        nonlocal txt2, s1
        txt2.updateContent(str(round(s1.getSliderState(), 2)))

    b1.quickSubscribeToHold(flashbang)
    b1.quickSubscribeToClick(getSliderValue)

    def stretch():
        nonlocal f4
        f4.setWidth(465)
        LayoutManager.applyLayout()

    def shrink():
        nonlocal f4
        f4.setWidth(340)
        LayoutManager.applyLayout()


    cb1.quickSubscribeToSelect(stretch)
    cb1.quickSubscribeToDeselect(shrink)

    toggle: bool = False
    def layoutMove():
        nonlocal toggle, f4
        if toggle:
            f4.alignpoint(Rect(), offset=20)
        else:
            f4.alignpoint(Rect(), offset=(200, 40))
        toggle = not toggle
        LayoutManager.applyLayout()

    tc1.quickSubscribeToState(3, layoutMove)

    # ------------------------- render ------------------------

    b2: Box = Box(Rect(size=(100, 100)), renderData=[BoxCO.COLOR2])
    b2.setZIndex(-1)

    allObjects: list[Renderer] = [l1, l2, ob2, txt1, f1, f4, f5, f6, b2, f8, dpd, sec1]
    while running:
        InputManager.update()

        main_screen.fill(background_color)
        allObjects = Renderer.renderAll(PygameSurface(main_screen), allObjects)

        pg.display.flip()
        background_color = 'black'

    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()

