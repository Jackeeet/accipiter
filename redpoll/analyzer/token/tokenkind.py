from enum import Enum


class TokenKind(str, Enum):
    IDENTIFIER = "идентификатор"
    TOOL_ID_START = "*"
    PROC_ID_START = "_"
    # block types
    OBJECTS = "объекты"
    TOOLS = "разметка"
    PROCESSING = "обработка"
    # tool types
    SEGMENT = "прямая"
    ARC = "кривая"
    AREA = "зона"
    LINE = "траектория"
    COUNTER = "счетчик"
    # general
    OR = "или"
    AND = "и"
    IF = "если"
    NUMBER = "число"
    STRING = "строка"
    COLOUR = "цвет"
    PARAM_NAME = "параметр"
    EVENT_NAME = "событие"
    ACTION_NAME = "действие"
    SIDE = "сторона"
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    COLON = ":"
    SEMICOLON = ";"
    EQUALS = "="
    COMMA = ","
    DOT = "."
    COORDS_START = "!"
    MINUS = "-"
    EOT = "EOT"
