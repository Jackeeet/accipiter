from enum import Enum


class DataType(Enum):
    COLOUR = "цвет"
    COMPOSITE = "составное",  # что составное? хороший вопрос
    COORDS = "координаты",
    FLOAT = "вещественное число",
    INT = "целое число",
    OBJECT_ID = "идентификатор (объект)",
    PROCESSING_ID = "идентификатор (событие/действие)"
    STRING = "строка",
    TOOL_ID = "идентификатор(инструмент)",
    POINT = "точка",
    SEGMENT = "прямая",
    ARC = "кривая",
    AREA = "зона",
    LINE = "линия",
    COUNTER = "счетчик",
    SIDE = "сторона",
    EVENT = "событие"
