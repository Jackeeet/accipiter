from videoanalytics.models import Coords, Shape


class Box(Shape):
    def __init__(
            self, start: Coords, width: int, height: int
    ) -> None:
        self.start = start
        self.width = width
        self.height = height

        self.top_left = start
        self.top_right = (self.start.x + width, self.start.y)
        self.bottom_right = (self.start.x + width, self.start.y + height)
        self.bottom_left = (self.start.x, self.start.y + height)
        super().__init__({
            self.top_left, self.top_right,
            self.bottom_left, self.bottom_right
        })
