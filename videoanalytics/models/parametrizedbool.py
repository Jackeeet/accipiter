from typing import Any


class ParametrizedBool:
    # class ParametrizedBool(Evaluable):

    # def evaluate(self, **values) -> bool:
    #     pass

    def __init__(self, value: bool, params: dict[str, Any] = None) -> None:
        self.bool = value
        self.params = params

    def __repr__(self) -> str:
        return f"ParametrizedBool({self.bool}, {self.params})"
