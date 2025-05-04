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

from ui import Framed, FramedCO
from ui import Stacked, Grouped, Dropdown
from ui import Section, SectionCO

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
    #screen: Box = Box(Rect(size=screen_size))
    main_screen = pg.display.set_mode(screen_size)
    background_color = 'black'

    
    # ----------------------- composite-elements ----------------------
    ob1: Box = Box(Rect(size=(100, 100)), renderData=[BoxCO.COLOR1])

    c1: TextCycle = TextCycle(Rect(), contents=[str(x) for x in range(5)], renderData=[TextCO.COLOR1])
    f1: Framed = Framed(c1, renderData=[LineCO.COLOR1])
    
    txts: list[Framed] = [Framed(Text(Rect(), content=str(x), renderData=[TextCO.COLOR1]), offset=10, renderData=[BoxCO.COLOR2]) for x in range(5)]
    stk1: Stacked = Stacked(Rect(size=(100, 50)), *txts, offset=10)

    out: Framed = Framed(Text(Rect(size=(200, 80)), content="SELECT", renderData=[TextCO.COLOR1]), renderData=[LineCO.COLOR2])
    txts2: list[Framed] = [Framed(Text(Rect(), content=str(x), renderData=[TextCO.COLOR1]), offset=10, renderData=[LineCO.COLOR1]) for x in range(5)]
    dpd: Dropdown = Dropdown(Rect(size=(100, 70)), out, (txts2[0], 0.5), (txts2[1], 1.2), *txts2[2:], offset=30)

    # ------------------------- layout ------------------------
    ob1.alignpoint(Rect(), offset=20)
    f1.alignpoint(ob1, otherPoint=(0, 1), offset=(0, 20))
    f1.setHeight(100)
    f1.setWidth(100)
    stk1.alignpoint(ob1, otherPoint=(1, 0), offset=(20, 0))
    dpd.alignpoint(stk1, otherPoint=(1, 0), offset=(20, 0))
    #stk1.setWidth(100)
    #stk1.setHeight(80)

    LayoutManager.applyLayout()
    #LayoutManager.applyLayout2()
    print(dpd.getRect())
    # ------------------------- action ------------------------

    def moveOBRight():
        nonlocal ob1, c1
        ob1.alignpoint(Rect(topleft=(120, 120)))
        #stk1.alignpoint(ob1, otherPoint=(1, 0), offset=(200, 20))
        stk1.setWidth(100)

    def moveOBLeft():
        nonlocal ob1
        ob1.alignpoint(Rect(topleft=(20, 20)))
        #stk1.alignpoint(ob1, otherPoint=(1, 0), offset=(20, 0))
        stk1.setWidth(300)

    c1.quickSubscribeToState(2, moveOBRight)
    c1.quickSubscribeToState(4, moveOBLeft)
    c1.quickSubscribeToClick(LayoutManager.applyLayout)



    # ------------------------- render ------------------------
    allObjects: list[Renderer] = [ob1, f1, stk1, dpd]
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

