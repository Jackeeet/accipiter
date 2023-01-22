import numpy as np


class Coords:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.xy = (x, y)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Coords):
            return self.x == o.x and self.y == o.y
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"Coords({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash(self.xy)

    def __add__(self, other) -> np.ndarray:
        return np.add(self, other)

    def __sub__(self, other) -> np.ndarray:
        return np.subtract(self, other)

    def __array__(self) -> np.ndarray:
        return np.array(self.xy)

    @staticmethod
    def from_array(arr: np.ndarray) -> 'Coords':
        assert len(arr) == 2
        return Coords(arr[0], arr[1])

    @staticmethod
    def from_tuple(tup: tuple[int, int]) -> 'Coords':
        assert len(tup) == 2
        return Coords(tup[0], tup[1])
