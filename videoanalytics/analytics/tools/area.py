from videoanalytics.analytics.tools.abstract import Component, Markup
from videoanalytics.models import Box


class Area(Markup):
    def __init__(self, components: list[Component], colour: tuple[int, int, int] = None, thickness: int = 2) -> None:
        super().__init__(colour, thickness)
        self._components = components
        for component in self._components:
            component.colour = self.colour
            component.thickness = self.thickness

    def draw_on(self, image) -> None:
        for tool in self._components:
            tool.draw_on(image)

    def contains(self, box: Box) -> bool:
        pass
