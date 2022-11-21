from typing import Any, Callable

from .tools import Counter
from support.detected_object import Tracked


class Action:
    def __init__(self, func: Callable, params: dict[str, Any]) -> None:
        self.func = func
        self.params = params

    def execute(self) -> None:
        self.func(**self.params)


def increment(counter: Counter) -> None:
    counter.increment()


def decrement(counter: Counter) -> None:
    counter.decrement()


def reset(counter: Counter) -> None:
    counter.reset()


def alert(message: str) -> None:
    print(f"alert: {message}")


def save(object: Tracked) -> None:
    print(f"saving: {object.obj.name} ({object.obj.box})")
