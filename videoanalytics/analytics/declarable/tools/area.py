from videoanalytics.analytics.declarable.tools import Tool


class Area(Tool):
    def __init__(self, contents: list[Tool], colour: tuple[int, int, int] = None, thickness: int = 2) -> None:
        super().__init__(colour, thickness)
        self._contents = contents
        for tool in self._contents:
            tool.colour = self.colour
            tool.thickness = self.thickness

    def draw_on(self, image):
        for tool in self._contents:
            tool.draw_on(image)
