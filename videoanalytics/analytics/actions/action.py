import queue
from typing import Callable, Any


class Action:
    def __init__(self, func: Callable, params: dict[str, Any]) -> None:
        self.func = func
        self.params = params

    def execute(self, output_queue: queue.Queue = None) -> None:
        if output_queue:
            self.params["output_queue"] = output_queue
        self.func(**self.params)
