from typing import Callable, Any


class Action:
    def __init__(self, func: Callable, params: dict[str, Any]) -> None:
        self.func = func
        self.params = params

    def execute(self) -> None:
        self.func(**self.params)
