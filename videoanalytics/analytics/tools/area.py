import numpy as np

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

        # only works for simple polygons (no self-intersections / holes)
        def check_convex() -> bool:
            vertex_count = len(self.vertices)
            sign = False
            for i in range(vertex_count):
                d1 = self.vertices[(i + 2) % vertex_count] - self.vertices[(i + 1) % vertex_count]
                d2 = self.vertices[i] - self.vertices[(i + 1) % vertex_count]
                clockwise = np.cross(np.asarray(d1), np.asarray(d2)) > 0
                if i == 0:
                    sign = clockwise
                elif sign != clockwise:
                    return False
            return True

        self.convex = check_convex()

    def draw_on(self, image) -> None:
        for tool in self._components:
            tool.draw_on(image)

    # this actually tests for collision, not for full containment
    # we'll probably need to find a way to differentiate these cases
    def contains(self, box: Box) -> bool:
        if not self.convex:
            raise NotImplementedError
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

    def __hash__(self) -> int:
        return hash((str(self.vertices), str(self._components)))

    def __eq__(self, o: object) -> bool:
        return self.vertices == o.vertices and self._components == o._components

