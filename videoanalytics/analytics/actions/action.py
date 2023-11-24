import queue
from typing import Callable, Any

from logmanager.logmanager import LogManager


class Action:
    def __init__(self, func: Callable, params: dict[str, Any]) -> None:
        self.func = func
        self.params = params

    def execute(self, output_queue: queue.Queue = None, logger: LogManager = None) -> None:
        if output_queue:
            self.params["output_queue"] = output_queue
        if logger:
            self.params["logger"] = logger
        self.func(**self.params)
