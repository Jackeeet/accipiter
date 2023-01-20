from abc import ABC, abstractmethod

from redpoll.expressions.attributes import Attributes
from redpoll.expressions.visitor import ExpressionVisitor


class Expr(ABC):
    """ The root of the class hierarchy."""

    def __init__(self):
        self.attrs = Attributes()

    @abstractmethod
    def accept(self, visitor: ExpressionVisitor): pass
