__all__ = ['BlockExpr', 'ObjectBlockExpr', 'ToolBlockExpr', 'ProcessingBlockExpr']

from abc import abstractmethod

from redpoll.expressions.blockitems import BlockItemExpr
from redpoll.expressions.expression import Expr
from redpoll.expressions.visitor import ExpressionVisitor


class BlockExpr(Expr):
    items: list[BlockItemExpr]

    @abstractmethod
    def __init__(self, line: int, pos: int) -> None:
        super().__init__(line, pos)
        self.items = []


class ObjectBlockExpr(BlockExpr):
    def __init__(self, line: int, pos: int) -> None:
        super().__init__(line, pos)

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_object_block(self)


class ToolBlockExpr(BlockExpr):
    def __init__(self, line: int, pos: int) -> None:
        super().__init__(line, pos)

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_tool_block(self)


class ProcessingBlockExpr(BlockExpr):
    def __init__(self, line: int, pos: int) -> None:
        super().__init__(line, pos)

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_processing_block(self)
