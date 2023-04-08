from typing import Any, Callable

from videoanalytics.interfaces.evaluable import Evaluable


class EvalTree(Evaluable):
    def __init__(
            self, left: Evaluable = None,
            op_or_val: Evaluable | str = None,
            right: Evaluable = None
    ) -> None:
        self.left = left
        self.operator_or_value = op_or_val
        self.right = right

    def evaluate(self, **values) -> Any:
        return self.fold(lambda ev: ev.evaluate(**values))

    def fold(self, func: Callable[[Any], Any]) -> Any:
        if self.left is None and self.right is None:
            return func(self.operator_or_value)
        if self.left is not None and self.right is not None:
            op = getattr(self.left.__class__, self.operator_or_value)
            return op(func(self.left), func(self.right))
        raise ValueError("missing an operand")

    def fmap(self, func: Callable[[Any], Any]) -> 'EvalTree':
        if self.left is None and self.right is None:
            return EvalTree(op_or_val=func(self.operator_or_value))
        if self.left is not None and self.right is not None:
            left = func(self.left)
            right = func(self.right)
            return EvalTree(left, self.operator_or_value, right)
        raise ValueError("missing an operand")

    def __repr__(self):
        return f"EvalTree({self.left}, {self.operator_or_value}, {self.right}"
