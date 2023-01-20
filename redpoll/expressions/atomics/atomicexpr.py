from abc import ABC, abstractmethod

from redpoll.expressions import ParamsExpr
from redpoll.types import DataType


class AtomicExpr(ParamsExpr, ABC):
    def __init__(self, value: tuple[int, int, int] | tuple[int, int] | float | int | str):
        super().__init__()
        self.value = value

    @property
    @abstractmethod
    def type(self) -> DataType: pass

    def __eq__(self, o: object) -> bool:
        if isinstance(o, AtomicExpr):
            return self.value == o.value
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __hash__(self):
        return self.value.__hash__()
