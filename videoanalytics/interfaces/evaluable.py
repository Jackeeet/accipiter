import abc
from typing import Any


class Evaluable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return hasattr(subclass, 'evaluate') and callable(subclass.evaluate) \
            and hasattr(subclass, 'op_and') and callable(subclass.op_and) \
            and hasattr(subclass, 'op_or') and callable(subclass.op_or) \
            or NotImplemented

    @abc.abstractmethod
    def evaluate(self, **values) -> Any:
        """ Вычисляет значение объекта.

        :param values: Значения, которые могут потребоваться для вычисления итогового значения объекта.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def op_and(left: Any, right: Any) -> Any:
        """ Эквивалент конъюнкции для результатов работы метода evaluate().

        :param left: Первое значение типа, возвращаемого методом evaluate()
        :param right: второе значение этого же типа.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def op_or(left: Any, right: Any) -> Any:
        """ Эквивалент дизъюнкции для результатов работы метода evaluate().

        :param left: Первое значение типа, возвращаемого методом evaluate()
        :param right:  второе значение этого же типа.
        """
        pass

    def __getattr__(self, key):
        match key:
            case "op_and":
                return self.op_and
            case "op_or":
                return self.op_or
            case "evaluate":
                return self.evaluate
            case _:
                raise AttributeError(key)
