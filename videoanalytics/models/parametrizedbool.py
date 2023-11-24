from typing import Any


class ParametrizedBool:
    def __init__(self, value: bool, params: dict[str, Any] = None) -> None:
        self.bool = value
        self.params = params

    def __repr__(self) -> str:
        return f"ParametrizedBool({self.bool}, {self.params})"
