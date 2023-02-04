import cv2

from videoanalytics.analytics.tools import Tool
from videoanalytics.models import Coords


class Counter(Tool):
    def __init__(self, start: int = 0, step: int = 1, draw: bool = False, origin: Coords = None,
                 colour: tuple[int, int, int] = None, thickness: int = 2):
        super().__init__(colour, thickness)
        self._origin = origin
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._scale = 1
        self._line = cv2.LINE_AA

        self._initial = start
        self._step = step
        self._draw = draw
        self.value = start

    def increment(self) -> None:
        self.value += self._step

    def decrement(self) -> None:
        self.value -= self._step

    def reset(self) -> None:
        self.value = self._initial

    def draw_on(self, image):
        cv2.putText(image, str(self.value), self._origin, self._font,
                    self._scale, self.colour, self.thickness, self._line)
