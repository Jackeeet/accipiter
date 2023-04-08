import abc
from typing import Any

from videoanalytics.interfaces import Evaluable


class Logical(Evaluable):
    @classmethod
    def __subclasshook(cls, subclass):
        return hasattr(subclass, 'op_and') and callable(subclass.op_and) \
            and hasattr(subclass, 'op_or') and callable(subclass.op_or) \
            or NotImplemented

    @staticmethod
    @abc.abstractmethod
    def op_and(left: Any, right: Any) -> Any:
        """ Эквивалент конъюнкции.

        :param left: Первое значение требуемого типа
        :param right: второе значение этого же типа.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def op_or(left: Any, right: Any) -> Any:
        """ Эквивалент дизъюнкции.

        :param left: Первое значение требуемого типа
        :param right:  второе значение этого же типа.
        """
        pass

    def __getattr__(self, key):
        match key:
            case "op_and":
                return self.op_and
            case "op_or":
                return self.op_or
            case _:
                raise AttributeError(key)
