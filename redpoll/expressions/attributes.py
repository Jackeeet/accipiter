from redpoll.types import DataType


# todo turn this into an abstract class
# and create separate attribute types for different expressions
# because e.g. atomics don't need a name
class Attributes:
    name: str
    names: set[str]  # идентификаторы в объявлениях
    filled_params: set[str]
    datatype: DataType
    value_types: set[DataType]

    def __init__(self):
        self.name = None
        self.names = set()
        self.filled_params = set()
        self.datatype = None
        self.value_types = set()
