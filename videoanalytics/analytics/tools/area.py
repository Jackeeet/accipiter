import math

import numpy as np

from videoanalytics.analytics.tools.abstract import Component, Markup
from videoanalytics.analytics.tools.helpers import translated_segment, connect
from videoanalytics.models import Box, Shape, Coords


class Area(Markup, Shape):
    def __init__(
            self, components: list[Component], colour: tuple[int, int, int] = None, thickness: int = 2
    ) -> None:
        super().__init__(colour=colour, thickness=thickness)
        self.vertices = []
        self._visible_components = components
        self._testing_components = []
        for component in self._visible_components:
            component.colour = self.colour
            component.thickness = self.thickness
            if component.start not in self.vertices:
                self.vertices.append(component.start)
            if component.end not in self.vertices:
                self.vertices.append(component.end)
            border = self.border_segment(component)
            if border == 0:
                self._testing_components.append(component)
            else:
                translated = translated_segment(component, border, 1000)
                self._testing_components.append(connect(component, translated))
                self._testing_components.append(translated_segment(component, border, 1000))
                self._testing_components.append(connect(component, translated, reverse=True))

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

    @staticmethod
    def border_segment(comp):
        left_vertical = comp.start.x == comp.end.x and comp.start.x == 0
        right_vertical = comp.start.x == comp.end.x and comp.start.x == 868
        top_horizontal = comp.start.y == comp.end.y and comp.start.y == 0
        bottom_horizontal = comp.start.y == comp.end.y and comp.start.y == 464
        if left_vertical:
            side = 4
        elif right_vertical:
            side = 2
        elif top_horizontal:
            side = 1
        elif bottom_horizontal:
            side = 3
        else:
            side = 0
        return side

    def draw_on(self, image) -> None:
        for tool in self._visible_components:
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
            for comp in self._testing_components:
                if self._ray_intersects_segment(point, comp):
                    ray_collision_count += 1
            if ray_collision_count % 2 == 0:
                return False
        return True

    @staticmethod
    def _ray_intersects_segment(point: Coords, line: Component) -> bool:
        if point == line.bounding_box.start or point == line.bounding_box.end:
            return True

        py = point.y
        px = point.x

        if py == line.bounding_box.start.y or py == line.bounding_box.end.y:
            py += 0.01

        if not (line.bounding_box.start.y < py < line.bounding_box.end.y):
            return False
        if px > line.bounding_box.end.x:
            return False
        if px < line.bounding_box.start.x:
            return True

        lower = line.start if line.start.y > line.end.y else line.end
        higher = line.end if line.start.y > line.end.y else line.start
        line_slope = math.inf \
            if lower.x == higher.x \
            else -1 * (higher.y - lower.y) / (higher.x - lower.x)
        point_slope = math.inf \
            if lower.x == point.x \
            else -1 * (py - lower.y) / (px - lower.x)
        return point_slope >= line_slope

    def _find_projections_axis_overlap(self, box, axes):
        for axis in axes:
            self_projection = self.projection(axis)
            box_projection = box.projection(axis)
            if not self_projection.overlaps(box_projection):
                return False
        return True

    def __hash__(self) -> int:
        return hash((str(self.vertices), str(self._visible_components)))

    def __eq__(self, o: object) -> bool:
        return self.vertices == o.vertices and self._visible_components == o._components
