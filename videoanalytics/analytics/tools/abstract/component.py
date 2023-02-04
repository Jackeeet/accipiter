from abc import ABC, abstractmethod

from videoanalytics.analytics.tools.abstract import Markup


class Component(Markup, ABC):
    def __init__(self, colour: tuple[int, int, int], thickness: int) -> None:
        super().__init__(colour, thickness)

    @property
    @abstractmethod
    def start(self): pass

    @property
    @abstractmethod
    def end(self): pass
