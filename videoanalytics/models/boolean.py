from videoanalytics.interfaces.logical import Logical


class Boolean(Logical):
    def __init__(self, value: bool) -> None:
        self.value = value

    def evaluate(self, **values) -> bool:
        return self.value

    @staticmethod
    def op_and(left: bool, right: bool) -> bool:
        return left and right

    @staticmethod
    def op_or(left: bool, right: bool) -> bool:
        return left or right
