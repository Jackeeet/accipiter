__all__ = ['IdentifierExpr', 'ObjectIdExpr', 'ToolIdExpr',
           'ProcessingIdExpr', 'ActionNameExpr', 'EventNameExpr']

from abc import abstractmethod

from redpoll.expressions.paramexpressions import ParamsExpr
from redpoll.expressions.visitor import ExpressionVisitor


class IdentifierExpr(ParamsExpr):
    @abstractmethod
    def __init__(self, line: int, pos: int, value: str) -> None:
        super().__init__(line, pos)
        if not isinstance(value, str):
            raise ValueError("Expected a value of type 'str'")
        self.value = value

    def __eq__(self, o: object) -> bool:
        if isinstance(o, IdentifierExpr):
            return self.value == o.value
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)


class ObjectIdExpr(IdentifierExpr):
    def __init__(self, line: int, pos: int, value: str) -> None:
        super().__init__(line, pos, value)

    def __repr__(self) -> str:
        return f"ObjectIdExpr({self.value})"

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_object_id(self)


class ToolIdExpr(IdentifierExpr):
    def __init__(self, line: int, pos: int, value: str) -> None:
        super().__init__(line, pos, value)

    def __repr__(self) -> str:
        return f"ToolIdExpr({self.value})"

    def __hash__(self):
        return self.value.__hash__()

    def accept(self, visitor):
        visitor.visit_tool_id(self)


class ProcessingIdExpr(IdentifierExpr):
    def __init__(self, line: int, pos: int, value: str) -> None:
        super().__init__(line, pos, value)

    def __repr__(self) -> str:
        return f"ProcessIdExpr({self.value})"

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_processing_id(self)


class ActionNameExpr(IdentifierExpr):
    def __init__(self, line: int, pos: int, value: str) -> None:
        super().__init__(line, pos, value)

    def __repr__(self) -> str:
        return f"ActionNameExpr({self.value})"

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_action_name(self)


class EventNameExpr(IdentifierExpr):
    def __init__(self, line: int, pos: int, value: str) -> None:
        super().__init__(line, pos, value)

    def __repr__(self) -> str:
        return f"EventNameExpr({self.value})"

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_event_name(self)
