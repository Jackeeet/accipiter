from typing import Any

from videoanalytics.interfaces.logical import Logical
from videoanalytics.models.operators import op_and, op_or


class MockEvent(Logical):
    def __init__(self, value: Any) -> None:
        self.value = value

    def evaluate(self, **values) -> Any:
        return self.value

    @staticmethod
    def op_and(left: Any, right: Any) -> Any:
        return op_and(left, right)

    @staticmethod
    def op_or(left: Any, right: Any) -> Any:
        return op_or(left, right)
