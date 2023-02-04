from typing import Callable

from videoanalytics.analytics.interfaces import Evaluable


class EvalTree(Evaluable):
    def __init__(
            self, left: Evaluable = None,
            op_or_val: Evaluable | Callable[[bool, bool], bool] = None,
            right: Evaluable = None
    ) -> None:
        self.left = left
        self.operator_or_value = op_or_val
        self.right = right

    def evaluate(self, **values) -> bool:
        if self.left is None and self.right is None:
            # the node is a leaf -> evaluate the value
            return self.operator_or_value.evaluate(**values)

        # the node is not a leaf -> evaluate both leaves and apply the operator
        if self.left is not None and self.right is not None:
            return self.operator_or_value(
                self.left.evaluate(**values), self.right.evaluate(**values)
            )

        raise ValueError("missing an operand")

    def flatten(self, func, result):
        if self.left is None and self.right is None:
            return func(self.operator_or_value, result)
        elif self.left is not None and self.right is not None:
            result = func(self.left, result)
            return func(self.right, result)
        else:
            raise ValueError("missing an operand")
