from abc import ABC

from videoanalytics.analytics.tools.abstract import Tool


class Markup(Tool, ABC):
    def __init__(self, colour: tuple[int, int, int], thickness: int, **kwargs) -> None:
        super().__init__(colour, thickness, **kwargs)
