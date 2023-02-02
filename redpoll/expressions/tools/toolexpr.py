from abc import ABC

from redpoll.expressions import BlockItemExpr, ToolIdExpr, ParamsExpr


class ToolExpr(BlockItemExpr, ABC):
    id: ToolIdExpr | None
    params: dict[str, ParamsExpr]

    def __init__(self, line: int, pos: int, name: ToolIdExpr = None) -> None:
        super().__init__(line, pos)
        self.id = name
        self.params = dict()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ToolExpr):
            return self.id == o.id
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)
