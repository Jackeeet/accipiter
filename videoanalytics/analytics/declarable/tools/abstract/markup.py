from abc import ABC

from videoanalytics.analytics.declarable.tools.abstract import Tool


class Markup(Tool, ABC):
    def __init__(self, colour: tuple[int, int, int], thickness: int) -> None:
        super().__init__(colour, thickness)
