from enum import Enum
from typing import Any, Callable
import pygame as pg

from .event import EventManager

class InputEvent(Enum):
    # ---------- digital-events ----------
    QUIT = 0

    MOUSEBUTTONDOWN = 100
    MOUSEBUTTONUP = 101

    LEFTDOWN = 104
    LEFTUP = 105

    A_DOWN = 200
    M_DOWN = 220
    
    # ---------- analog-events ----------
    UPDATE = 1000
    LEFTHELD = 1100

class InputManager:
    events: dict[InputEvent, str] = {}
    currentDown: set[InputEvent] = set()

    @staticmethod
    def init() -> None:
        for event in list(InputEvent):
            InputManager.events[event] = EventManager.createEvent()


    @staticmethod
    def update() -> None:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    EventManager.triggerEvent(InputManager.events[InputEvent.QUIT])
                case pg.KEYDOWN:
                    if pg.key.get_pressed()[pg.K_ESCAPE]:
                        EventManager.triggerEvent(InputManager.events[InputEvent.QUIT])
                    if pg.key.get_pressed()[pg.K_a]:
                        EventManager.triggerEvent(InputManager.events[InputEvent.A_DOWN])
                    if pg.key.get_pressed()[pg.K_m]:
                        EventManager.triggerEvent(InputManager.events[InputEvent.M_DOWN])
                case pg.MOUSEBUTTONDOWN:
                    EventManager.triggerEvent(InputManager.events[InputEvent.MOUSEBUTTONDOWN])
                    if InputEvent.LEFTHELD not in InputManager.currentDown and pg.mouse.get_pressed()[0]:
                        EventManager.triggerEvent(InputManager.events[InputEvent.LEFTDOWN])
                        InputManager.currentDown.add(InputEvent.LEFTHELD)

                case pg.MOUSEBUTTONUP:
                    EventManager.triggerEvent(InputManager.events[InputEvent.MOUSEBUTTONUP])
                    if InputEvent.LEFTHELD in InputManager.currentDown and not pg.mouse.get_pressed()[0]:
                        EventManager.triggerEvent(InputManager.events[InputEvent.LEFTUP])
                        InputManager.currentDown.remove(InputEvent.LEFTHELD)

        #for event in InputManager.currentDown:
        #    EventManager.triggerEvent(InputManager.events[event])

        EventManager.triggerEvent(InputManager.events[InputEvent.UPDATE])

    @staticmethod
    def getEvent(event: InputEvent) -> str:
        if InputManager.events.get(event):
            return InputManager.events[event]
        return ''

    @staticmethod
    def subscribeToEvent(event: InputEvent, callback: str) -> bool:
        if InputManager.events.get(event):
            return EventManager.subscribeToEvent(InputManager.events[event], callback)
        return False

    @staticmethod
    def quickSubscribe(event: InputEvent, f: Callable, *args: Any) -> bool:
        if InputManager.events.get(event):
            return EventManager.quickSubscribe(InputManager.events[event], f, *args)[1]
        return False

    @staticmethod
    def getMousePosition() -> tuple[int, int]:
        return pg.mouse.get_pos()

