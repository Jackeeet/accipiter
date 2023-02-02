from redpoll.expressions import Expr


class SemanticError(Exception):
    def __init__(self, expr: Expr, message: str):
        self.expr = expr
        self.message = f"[{expr.line}:{expr.position}] {message}"
        super().__init__(self.message)
