import math

import numpy as np

from videoanalytics.analytics.tools.abstract import Component, Markup
from videoanalytics.models import Box, Shape, Coords


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

    def overlaps(self, box: Box) -> bool:
        if not self.convex:
            raise NotImplementedError
        overlap_on_self_axes = self._find_projections_axis_overlap(box, self.axes())
        if not overlap_on_self_axes:
            return False
        overlap_on_all_axes = self._find_projections_axis_overlap(box, box.axes())
        return overlap_on_all_axes

    def contains(self, box: Box) -> bool:
        for point in box.points:
            ray_collision_count = 0
            for comp in self._components:
                if self._ray_intersects_segment(point, comp):
                    ray_collision_count += 1
            if ray_collision_count % 2 == 0:
                return False
        return True

    @staticmethod
    def _ray_intersects_segment(point: Coords, line: Component) -> bool:
        if not (line.bounding_box.start.y <= point.y <= line.bounding_box.end.y):
            return False
        if point.x > line.bounding_box.end.x:
            return False
        if point.x < line.bounding_box.start.x:
            return True

        lower = line.start if line.start.y > line.end.y else line.end
        higher = line.end if line.start.y > line.end.y else line.start
        line_slope = math.inf \
            if lower.x == higher.x \
            else -1 * (higher.y - lower.y) / (higher.x - lower.x)
        point_slope = math.inf \
            if lower.x == point.x \
            else -1 * (point.y - lower.y) / (point.x - lower.x)
        return point_slope >= line_slope

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
