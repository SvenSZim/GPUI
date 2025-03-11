from enum import Enum
from typing import Any, Callable
import pygame as pg

from .eventmanager import EventManager

class InputEvent(Enum):
    QUIT = 0

    MOUSEBUTTONDOWN = 100
    MOUSEBUTTONUP = 101

    A_DOWN = 200

class InputManager:
    events: dict[InputEvent, str] = {}

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
                case pg.MOUSEBUTTONDOWN:
                    EventManager.triggerEvent(InputManager.events[InputEvent.MOUSEBUTTONDOWN])
                case pg.MOUSEBUTTONUP:
                    EventManager.triggerEvent(InputManager.events[InputEvent.MOUSEBUTTONUP])

    @staticmethod
    def getEvent(event: InputEvent) -> str:
        if InputManager.events.get(event):
            return InputManager.events[event]
        return ''

    @staticmethod
    def subscribeToEvent(event: InputEvent, f: Callable, *args: Any) -> bool:
        if InputManager.events.get(event):
            return EventManager.subscribeToEvent(InputManager.events[event], f, *args)
        return False


