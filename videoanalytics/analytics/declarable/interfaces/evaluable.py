import abc


class Evaluable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return hasattr(subclass, 'evaluate') \
            and callable(subclass.evaluate) \
            or NotImplemented

    @abc.abstractmethod
    def evaluate(self, **values) -> bool: pass
