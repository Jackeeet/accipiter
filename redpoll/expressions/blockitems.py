__all__ = ['BlockItemExpr', 'ObjectExpr',
           'ProcessingExpr', 'ConditionExpr', 'DeclarationExpr']

from abc import abstractmethod

from redpoll.expressions.expression import Expr
from redpoll.expressions.declarable import DeclarableExpr, ActionExpr, EventExpr
from redpoll.expressions.binaryexpr import BinaryExpr
from redpoll.expressions.identifiers import ObjectIdExpr, ProcessingIdExpr
from redpoll.expressions.visitor import ExpressionVisitor


class BlockItemExpr(Expr):
    """ Expressions that can be used in one of the three blocks. """

    @abstractmethod
    def __init__(self, line: int, pos: int) -> None:
        super().__init__(line, pos)


class ObjectExpr(BlockItemExpr):
    def __init__(self, line: int, pos: int, obj_id: ObjectIdExpr = None) -> None:
        super().__init__(line, pos)
        self.id = obj_id

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ObjectExpr):
            return self.id == o.id
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self):
        return f"ObjectExpr({self.id})"

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_object(self)


class ProcessingExpr(BlockItemExpr):
    """ Expressions that can be used in the 'processing' block. """

    @abstractmethod
    def __init__(self, line: int, pos: int) -> None:
        super().__init__(line, pos)


class ConditionExpr(ProcessingExpr):
    event: EventExpr | ProcessingIdExpr | BinaryExpr | None
    actions: list[ActionExpr | ProcessingIdExpr]

    def __init__(self, line: int, pos: int, event: EventExpr | ProcessingIdExpr = None) -> None:
        super().__init__(line, pos)
        self.event = event
        self.actions = []

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ConditionExpr):
            return self.event == o.event and self.actions == o.actions
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({self.event})"

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_condition(self)


class DeclarationExpr(ProcessingExpr):
    def __init__(
            self, line: int, pos: int, name: ProcessingIdExpr = None, body: DeclarableExpr = None
    ) -> None:
        super().__init__(line, pos)
        self.name = name
        self.body = body

    def __eq__(self, o: object) -> bool:
        if isinstance(o, DeclarationExpr):
            return self.name == o.name and self.body == o.body
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({self.name}, {self.body})"

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_declaration(self)
