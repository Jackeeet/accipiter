from videoanalytics.analytics.declarable.tools.abstract import Component, Markup


class Area(Markup):
    def __init__(self, contents: list[Component], colour: tuple[int, int, int] = None, thickness: int = 2) -> None:
        super().__init__(colour, thickness)
        self._components = contents
        for component in self._components:
            component.colour = self.colour
            component.thickness = self.thickness

    def draw_on(self, image):
        for tool in self._components:
            tool.draw_on(image)
