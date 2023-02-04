import abc


class Intersectable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'intersects') \
            and callable(subclass.intersects) \
            or NotImplemented

    @abc.abstractmethod
    def intersects(self, segment) -> bool:
        """ Определяет, пересекает ли отрезок данный объект.

        :param segment: Отрезок
        """
        pass
