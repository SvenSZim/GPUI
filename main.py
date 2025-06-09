from time import perf_counter
import pygame as pg
import numpy as np

from pygamesetup import PygameDrawer, PygameSurface, PygameFont, PygameInputHandler

from ui import Parser, InputManager, InputEvent, UI

from exampleEngine import Engine

def main():
    pg.init()
    pg.font.init()

    # ------------------------------ setup ------------------------------
    running: bool = True

    def quit():
        nonlocal running
        running = False

    screen_size: tuple[int, int] = (1280, 720)
    main_screen: pg.Surface = pg.display.set_mode(screen_size)

    # physics-setup
    physicsEngine: Engine = Engine(np.array(screen_size)/2, np.float64(min(screen_size)/2.6), np.float64(25))
    
    # ui-setup
    InputManager.init(PygameInputHandler)   # initialize ui-input module
    InputManager.quickSubscribe(InputEvent.QUIT, quit)
    
    UI.init(PygameDrawer, PygameFont)   # initialize ui-rendering module
    
    Parser.loadStyleFromXML("styleexample.xml")             # load style
    Parser.setDefaultStyle('moon')                          # set style
    ui: UI = Parser.loadLayoutFromXML("layoutexample.xml")  # load layout
    ui.setSize(screen_size)                                 # set layout size

    # set colors of gravity cycle
    ui.getElementByID("gravityMode").set({'boxcolor':'gray'},sets=1)
    ui.getElementByID("gravityMode").set({'boxcolor':'darkred'},sets=1,skips=[1])
    ui.getElementByID("gravityMode").set({'boxcolor':'blue'},sets=1,skips=[2])

    # button functionality
    def addObject():
        nonlocal physicsEngine
        physicsEngine.addObject(np.array(screen_size)/2 + np.array([100, -100]), np.zeros(2))

    ui.getElementByID('addObject').set({'quickSubscribeToClick':(addObject, [])})
    ui.getElementByID('tpObjects').set({'quickSubscribeToClick':(physicsEngine.applyRandomTeleports, [350.0])})
    ui.getElementByID('toggleCollisions').set({'quickSubscribeToClick':(physicsEngine.toggleCollisions, [])})
    ui.getElementByID('toggleRandomRad').set({'quickSubscribeToClick':(physicsEngine.toggleRandomRadOff, [])})
    [ui.getElementByID('gravityMode').set({'quickSubscribeToToggleState':(x, physicsEngine.setGravityMode, [x])}) for x in range(3)]
    ui.getElementByID('clearObjects').set({'quickSubscribeToClick':(physicsEngine.clear, [])})

    # ------------------------------ runtime-loop ------------------------------
    last_frame_time: float = perf_counter()

    while running:
        # input update
        InputManager.update()

        # physics update
        dt: float = perf_counter() - last_frame_time
        last_frame_time = perf_counter()
        physicsEngine.update(np.float64(dt))

        # ui update
        fps = round(1/dt, 2)
        ui.getElementByID('fps').set({'content':f'{fps}'},sets=1,skips=[1])
        ui.getElementByID('balls').set({'content':f'{len(physicsEngine.getAllObjectPositions())}'},sets=1,skips=[1])

        # rendering
        main_screen.fill("black")

        # physics rendering
        pg.draw.circle(main_screen, "red", [int(x) for x in physicsEngine.worldcenter[:2]], int(physicsEngine.worldrad), width=1)
        for pos, rad in physicsEngine.getAllObjectPositions():
            pg.draw.circle(main_screen, "white", [int(x) for x in pos[:2]], int(rad))
        
        # ui rendering
        ui.render(PygameSurface(main_screen))

        pg.display.flip()


    pg.font.quit()
    pg.quit()



if __name__ == '__main__':
    main()

