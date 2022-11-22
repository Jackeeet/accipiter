from typing import Any, Callable

from .tools import Counter
from support.detected_object import Tracked


class Action:
    def __init__(self, func: Callable, params: dict[str, Any]) -> None:
        self.func = func
        self.params = params

    def execute(self) -> None:
        self.func(**self.params)


def increment(counter: Counter, object: Tracked = None) -> None:
    counter.increment()


def decrement(counter: Counter, object: Tracked = None) -> None:
    counter.decrement()


def reset(counter: Counter, object: Tracked = None) -> None:
    counter.reset()


def alert(message: str, object: Tracked = None) -> None:
    print(f"alert: {message}")


def save(object: Tracked) -> None:
    print(f"saving: {object.obj.name} ({object.obj.box})")


def set_colour(colour: tuple[int, int, int], object: Tracked) -> None:
    object.obj.colour = colour
