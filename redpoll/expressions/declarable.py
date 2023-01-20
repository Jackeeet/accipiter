__all__ = ['DeclarableExpr', 'ActionExpr', 'EventExpr']

from abc import abstractmethod

from redpoll.expressions.expr import Expr
from redpoll.expressions.identifiers import ActionNameExpr, EventNameExpr, ObjectIdExpr, ToolIdExpr
from redpoll.expressions.paramexpressions import ParamsExpr
from redpoll.expressions.visitor import ExpressionVisitor


class DeclarableExpr(Expr):
    """ Expressions that can be used as declaration bodies in the processing block."""
    args: list[ParamsExpr]

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.args = []

    def __eq__(self, o: object) -> bool:
        if isinstance(o, DeclarableExpr):
            return self.args == o.args
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__ne__(o)


class ActionExpr(DeclarableExpr):
    name: ActionNameExpr | None

    def __init__(self, name: ActionNameExpr = None) -> None:
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
    name: EventNameExpr | None

    def __init__(self, target: ObjectIdExpr | ToolIdExpr = None, event: EventNameExpr = None) -> None:
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
