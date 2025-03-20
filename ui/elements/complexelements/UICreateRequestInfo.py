from abc import ABC
from dataclasses import dataclass
from typing import Union

@dataclass
class UIABCCreateRequestInfo(ABC):
    id: str = ''
    pass


@dataclass
class UITextCreateRequestInfo(UIABCCreateRequestInfo):
    content: str = ''


@dataclass
class UIButtonCreateRequestInfo(UIABCCreateRequestInfo):
    numberOfStates: int = 2
    startState: int = 0
