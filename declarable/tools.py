import cv2
from abc import ABC, abstractmethod
from collections import namedtuple

Coords = namedtuple("Coords", "x y")

Box = namedtuple("Box", "start width height")


class Tool(ABC):
    def __init__(self, colour: tuple[int, int, int], thickness: int) -> None:
        self.colour = colour or (0, 0, 0)
        self.thickness = thickness or 1

    @abstractmethod
    def draw_on(self, image): pass


class Point(Tool):
    def __init__(self, coords: Coords, colour: tuple[int, int, int] = None, thickness: int = 2) -> None:
        self.coords = coords
        super().__init__(colour, thickness)

    def draw_on(self, image):
        cv2.circle(image, self.coords, radius=0,
                   color=self.colour, thickness=self.thickness)


class Segment(Tool):
    def __init__(self, start: Coords, end: Coords, colour: tuple[int, int, int] = None, thickness: int = 2) -> None:
        self.start = start
        self.end = end
        super().__init__(colour, thickness)

    def draw_on(self, image):
        cv2.line(image, self.start, self.end,
                 self.colour, thickness=self.thickness)


class Curve(Tool):
    pass


class Area(Tool):
    pass


class Line(Tool):  # this is the old trajectory
    pass


class Counter(Tool):
    def __init__(self, initial: int = 0, step: int = 1, draw: bool = False, origin: Coords = None, colour: tuple[int, int, int] = None, thickness: int = 2):
        super().__init__(colour, thickness)
        self._origin = origin
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._scale = 1
        self._line = cv2.LINE_AA

        self._initial = initial
        self._step = step
        self._draw = draw
        self.value = initial

    def increment(self) -> None:
        self.value += self._step

    def decrement(self) -> None:
        self.value -= self._step

    def reset(self) -> None:
        self.value = self._initial

    def draw_on(self, image):
        cv2.putText(image, str(self.value), self._origin, self._font, self._scale, self.colour, self.thickness, self._line)
