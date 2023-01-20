__all__ = ['AtomicExpr', 'ColourExpr', 'CoordsExpr',
           'FloatExpr', 'IntExpr', 'StringExpr']

from abc import ABC, abstractmethod

from redpoll.expressions import ParamsExpr, ExpressionVisitor
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


class ColourExpr(AtomicExpr):
    def __init__(self, value: tuple[int, int, int]) -> None:
        assert isinstance(value, tuple)
        assert len(value) == 3
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.COLOUR

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_colour(self)


class CoordsExpr(AtomicExpr):
    def __init__(self, value: tuple[int, int]) -> None:
        assert isinstance(value, tuple)
        assert len(value) == 2
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.COORDS

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_coords(self)


class FloatExpr(AtomicExpr):
    def __init__(self, value: float) -> None:
        assert isinstance(value, float)
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.FLOAT

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_float(self)


class IntExpr(AtomicExpr):
    def __init__(self, value: int) -> None:
        assert isinstance(value, int)
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.INT

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_int(self)


class StringExpr(AtomicExpr):
    def __init__(self, value: str) -> None:
        assert isinstance(value, str)
        super().__init__(f"'{value}'")

    @property
    def type(self) -> DataType:
        return DataType.STRING

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_string(self)
