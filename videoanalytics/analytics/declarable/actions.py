from typing import Any, Callable

from .tools import Counter
from ...models import Tracked


class Action:
    def __init__(self, func: Callable, params: dict[str, Any]) -> None:
        self.func = func
        self.params = params

    def execute(self) -> None:
        self.func(**self.params)


def increment(counter: Counter, tracked: Tracked = None) -> None:
    counter.increment()


def decrement(counter: Counter, tracked: Tracked = None) -> None:
    counter.decrement()


def reset(counter: Counter, tracked: Tracked = None) -> None:
    counter.reset()


def alert(message: str, tracked: Tracked = None) -> None:
    print(f"alert: {message}")


def save(tracked: Tracked) -> None:
    print(f"saving: {tracked.obj.name} ({tracked.obj.box})")


def set_colour(colour: tuple[int, int, int], tracked: Tracked) -> None:
    tracked.obj.colour = colour
