from abc import ABC

import numpy as np

from videoanalytics.models.projection import Projection


class Shape(ABC):
    def __init__(self, vertices: list[tuple[int, int]], **kwargs):
        self.vertices = vertices

    def axes(self) -> list[np.ndarray]:
        max_vertex_index = len(self.vertices) - 1
        vertices = self.vertices
        axes = []
        for i, vertex in enumerate(vertices):
            p1 = vertex
            p2 = vertices[0] if i == max_vertex_index else vertices[i + 1]
            edge: np.ndarray = np.subtract(p1, p2)
            axes.append(np.asarray((-edge[1], edge[0])))
        return axes

    def projection(self, axis: np.ndarray) -> Projection:
        projections = [axis.dot(np.asarray(vertex)) for vertex in self.vertices]
        return Projection(min(projections), max(projections))
