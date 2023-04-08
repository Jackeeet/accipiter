import abc
from typing import Any


class Evaluable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return hasattr(subclass, 'evaluate') and callable(subclass.evaluate) \
            or NotImplemented

    @abc.abstractmethod
    def evaluate(self, **values) -> Any:
        """ Вычисляет значение объекта.

        :param values: Значения, которые могут потребоваться для вычисления итогового значения объекта.
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
