__all__ = ['BlockExpr', 'ObjectBlockExpr', 'ToolBlockExpr', 'ProcessingBlockExpr']

from abc import abstractmethod

from redpoll.expressions.blockitems import BlockItemExpr
from redpoll.expressions.expression import Expr
from redpoll.expressions.visitor import ExpressionVisitor


class BlockExpr(Expr):
    items: list[BlockItemExpr]

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.items = []


class ObjectBlockExpr(BlockExpr):
    def __init__(self) -> None:
        super().__init__()

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_object_block(self)


class ToolBlockExpr(BlockExpr):
    def __init__(self) -> None:
        super().__init__()

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_tool_block(self)


class ProcessingBlockExpr(BlockExpr):
    def __init__(self) -> None:
        super().__init__()

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_processing_block(self)
