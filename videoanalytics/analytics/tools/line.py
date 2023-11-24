from videoanalytics.analytics.tools.abstract import Component, Markup
from videoanalytics.analytics.tools.interfaces import Intersectable


class Line(Markup, Intersectable):
    def __init__(self, components: list[Component], colour: tuple[int, int, int] = None, thickness: int = 2):
        super().__init__(colour, thickness)
        self._components = components
        for component in self._components:
            component.colour = self.colour
            component.thickness = self.thickness

    def draw_on(self, image) -> None:
        for component in self._components:
            component.draw_on(image)

    def intersects(self, segment) -> bool:
        for component in self._components:
            if not isinstance(component, Intersectable):
                raise ValueError
            if component.intersects(segment):
                return True
        return False
