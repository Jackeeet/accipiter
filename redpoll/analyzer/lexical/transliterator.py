from enum import Enum


class Symbol(Enum):
    LETTER = "А-Яа-я"
    LATIN_LETTER = "A-Za-z"
    NUMBER = "0-9"
    UNDERSCORE = "_"
    STAR = "*"
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    EXCLAMATION = "!"
    COLON = ":"
    SEMICOLON = ";"
    EQUALS = "="
    COMMA = ","
    DOT = "."
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = "\""
    MINUS = "-"
    BLANK = " "
    UNKNOWN = "?"
    EOL = "\n"
    EOT = "EOT"


class Transliterator:
    _lut = {
        '*': Symbol.STAR,
        '_': Symbol.UNDERSCORE,
        '(': Symbol.LEFT_BRACKET,
        ')': Symbol.RIGHT_BRACKET,
        ':': Symbol.COLON,
        ';': Symbol.SEMICOLON,
        '=': Symbol.EQUALS,
        ',': Symbol.COMMA,
        '.': Symbol.DOT,
        '-': Symbol.MINUS,
        '!': Symbol.EXCLAMATION,
        '"': Symbol.DOUBLE_QUOTE,
        '\'': Symbol.SINGLE_QUOTE,
        '\n': Symbol.EOL
    }

    def __init__(self, source_text: str):
        self._source = source_text
        self._source_len = len(self._source)
        self._curr_index = -1

        self.line = 1
        self.position = 0
        self.symbol = None

    @property
    def char(self):
        return self._source[self._curr_index]

    def read_next(self) -> None:
        self._curr_index += 1
        if self._curr_index >= self._source_len:
            self.symbol = Symbol.EOT
            self.position += 1
            return

        self._classify()
        if self.symbol == Symbol.EOL:
            self.line += 1
            self.position = 0
        else:
            self.position += 1

    def _classify(self) -> None:
        if self.char in self._lut:
            self.symbol = self._lut[self.char]
        elif self.char.isdecimal():
            self.symbol = Symbol.NUMBER
        elif self.char.isspace():
            self.symbol = Symbol.BLANK
        elif Transliterator._is_latin(self.char):
            self.symbol = Symbol.LATIN_LETTER
        elif Transliterator._is_cyrillic(self.char):
            self.symbol = Symbol.LETTER
        else:
            self.symbol = Symbol.UNKNOWN

    @staticmethod
    def _is_latin(ch: str) -> bool:
        return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'

    @staticmethod
    def _is_cyrillic(ch: str) -> bool:
        return 'а' <= ch <= 'я' or 'А' <= ch <= 'Я' or ch == 'ё' or ch == 'Ё'
