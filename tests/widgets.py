from dataclasses import dataclass, field
from typing import List
from types import FunctionType


@dataclass
class Widget:
    layout: object = None


@dataclass
class Label:
    text: str = None


@dataclass
class Text:
    text: str = None


@dataclass
class Button:
    pressed: FunctionType = field(default=None, compare=False)


@dataclass
class Layout:
    widgets: List[object] = field(default_factory=list)


@dataclass
class VLayout(Layout):
    pass


@dataclass
class HLayout(Layout):
    pass
