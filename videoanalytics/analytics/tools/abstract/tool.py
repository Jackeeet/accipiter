from abc import ABC, abstractmethod


class Tool(ABC):
    def __init__(self, colour: tuple[int, int, int], thickness: int) -> None:
        # reversed() call is necessary because openCV uses BGR and not RGB
        self.colour = (0, 0, 0) if colour is None else tuple(reversed(colour))
        self.thickness = thickness or 1

    @abstractmethod
    def draw_on(self, image) -> None: pass

    # @abstractmethod
    # def __hash__(self) -> int:
    #     pass

