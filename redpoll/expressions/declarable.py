__all__ = ['DeclarableExpr', 'ActionExpr', 'EventExpr']

from abc import abstractmethod

from .expression import Expr
from .identifiers import ActionIdExpr, EventIdExpr, ObjectIdExpr, ToolIdExpr
from .paramexpressions import ParamsExpr
from .visitor import ExpressionVisitor


class DeclarableExpr(Expr):
    """ Expressions that can be used as declaration bodies in the processing block."""
    params: dict[str, ParamsExpr]

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.params = dict()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, DeclarableExpr):
            return self.params == o.params
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__ne__(o)


class ActionExpr(DeclarableExpr):
    name: ActionIdExpr | None

    def __init__(self, name: ActionIdExpr = None) -> None:
        self.name = name
        super().__init__()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ActionExpr):
            return self.name == o.name and super().__eq__(o)
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__ne__(o)

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({self.name})"

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_action(self)


class EventExpr(DeclarableExpr):
    target: ObjectIdExpr | ToolIdExpr | None
    name: EventIdExpr | None

    def __init__(self, target: ObjectIdExpr | ToolIdExpr = None, event: EventIdExpr = None) -> None:
        self.target = target
        self.name = event
        super().__init__()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, EventExpr):
            return self.target == o.target and self.name == o.name and super().__eq__(o)
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({self.target}, {self.name})"

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_event(self)
