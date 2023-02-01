from enum import Enum


class DataType(Enum):
    ARC = "дуга",
    AREA = "зона",
    COLOUR = "цвет"
    COMPOSITE = "состав",  # тип параметра инструмента "состав"
    COORDS = "координаты",
    COUNTER = "счетчик",
    EVENT = "событие",
    FLOAT = "вещественное число",
    INT = "целое число",
    LINE = "линия",
    OBJECT_ID = "идентификатор (объект)",
    POINT = "точка",
    PROCESSING_ID = "идентификатор (событие/действие)"
    SEGMENT = "прямая",
    SIDE = "сторона",
    STRING = "строка",
    TOOL_ID = "идентификатор(инструмент)",
