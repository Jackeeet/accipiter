from redpoll.expressions import Expr, ObjectBlockExpr, ToolBlockExpr, ProcessingBlockExpr, ExpressionVisitor


class ProgramExpr(Expr):
    def __init__(self, o: ObjectBlockExpr = None, t: ToolBlockExpr = None, p: ProcessingBlockExpr = None) -> None:
        super().__init__()
        self.objects = o
        self.tools = t
        self.processing = p

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_program(self)
