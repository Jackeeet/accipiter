from abc import ABC, abstractmethod


class Tool(ABC):
    def __init__(self, colour: tuple[int, int, int], thickness: int) -> None:
        self.colour = colour or (0, 0, 0)
        self.thickness = thickness or 1

    @abstractmethod
    def draw_on(self, image): pass
