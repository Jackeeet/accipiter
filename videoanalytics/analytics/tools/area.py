from videoanalytics.analytics.tools.abstract import Component, Markup
from videoanalytics.models import Box, Shape


class Area(Markup, Shape):
    def __init__(
            self, components: list[Component], colour: tuple[int, int, int] = None, thickness: int = 2
    ) -> None:
        super().__init__(colour=colour, thickness=thickness)
        self.vertices = []
        self._components = components
        for component in self._components:
            component.colour = self.colour
            component.thickness = self.thickness
            if component.start not in self.vertices:
                self.vertices.append(component.start)
            if component.end not in self.vertices:
                self.vertices.append(component.end)

        self.convex = None

    def draw_on(self, image) -> None:
        for tool in self._components:
            tool.draw_on(image)

    # this actually tests for collison, not for a full containment
    # we'll probably need to find a way to differentiate these cases
    def contains(self, box: Box) -> bool:
        if not self.convex:
            pass
        overlap_on_self_axes = self._find_projections_axis_overlap(box, self.axes())
        if not overlap_on_self_axes:
            return False
        overlap_on_all_axes = self._find_projections_axis_overlap(box, box.axes())
        return overlap_on_all_axes

    def _find_projections_axis_overlap(self, box, axes):
        for axis in axes:
            self_projection = self.projection(axis)
            box_projection = box.projection(axis)
            if not self_projection.overlaps(box_projection):
                return False
        return True
