from redpoll.analyzer.lexical.lexererror import LexerError
from redpoll.analyzer.lexical.state import State
from redpoll.analyzer.lexical.transliterator import Symbol, Transliterator
from redpoll.analyzer.token import Token, TokenKind
from redpoll.resources import keywords as kw


class Lexer:
    _keywords: dict[str, TokenKind]
    _deltas: dict[State, dict[Symbol, State]]
    _1char_tokens: dict[Symbol, TokenKind]
    _id_key_starters: set[Symbol]
    _skippable: set[Symbol]
    _tlr: Transliterator
    _token_value: list[str]
    _state: State

    def __init__(self, source_text: str) -> None:
        self._skippable = {Symbol.BLANK, Symbol.EOL}
        self._identifier_chars = {
            Symbol.LETTER, Symbol.LATIN_LETTER,
            Symbol.UNDERSCORE, Symbol.NUMBER
        }
        self._keywords = {
            # logic / control flow
            kw.IF: TokenKind.IF,
            kw.OR: TokenKind.OR,
            kw.AND: TokenKind.AND,
            # block types
            kw.OBJECTS: TokenKind.OBJECTS,
            kw.TOOLS: TokenKind.TOOLS,
            kw.PROCESSING: TokenKind.PROCESSING,
            # tool types
            kw.SEGMENT: TokenKind.SEGMENT,
            kw.ARC: TokenKind.ARC,
            kw.AREA: TokenKind.AREA,
            kw.LINE: TokenKind.LINE,
            kw.COUNTER: TokenKind.COUNTER,
            # tool parameter names
            kw.COMPONENTS: TokenKind.PARAM_NAME,
            kw.FROM: TokenKind.PARAM_NAME,
            kw.TO: TokenKind.PARAM_NAME,
            kw.ANGLE_FROM: TokenKind.PARAM_NAME,
            kw.ANGLE_TO: TokenKind.PARAM_NAME,
            kw.COLOUR: TokenKind.PARAM_NAME,
            kw.THICKNESS: TokenKind.PARAM_NAME,
            kw.CENTER: TokenKind.PARAM_NAME,
            kw.RADIUS: TokenKind.PARAM_NAME,
            kw.START: TokenKind.PARAM_NAME,
            kw.STEP: TokenKind.PARAM_NAME,
            # event names
            kw.CROSSING: TokenKind.EVENT_NAME,
            kw.ENTERING: TokenKind.EVENT_NAME,
            kw.LEAVING: TokenKind.EVENT_NAME,
            kw.DIVERTS_FROM: TokenKind.EVENT_NAME,
            kw.SPEEDING_UP: TokenKind.EVENT_NAME,
            kw.SLOWING_DOWN: TokenKind.EVENT_NAME,
            kw.STILL: TokenKind.EVENT_NAME,
            kw.APPEARS: TokenKind.EVENT_NAME,
            kw.DISAPPEARS: TokenKind.EVENT_NAME,
            kw.EQUALS: TokenKind.EVENT_NAME,
            kw.ABOVE: TokenKind.EVENT_NAME,
            # action names
            kw.ALERT: TokenKind.ACTION_NAME,
            kw.SAVE: TokenKind.ACTION_NAME,
            kw.INCREMENT: TokenKind.ACTION_NAME,
            kw.DECREMENT: TokenKind.ACTION_NAME,
            kw.RESET: TokenKind.ACTION_NAME,
            kw.FLASH: TokenKind.ACTION_NAME,
            # constants
            kw.SIDE_LEFT: TokenKind.SIDE,
            kw.SIDE_TOP: TokenKind.SIDE,
            kw.SIDE_RIGHT: TokenKind.SIDE,
            kw.SIDE_BOTTOM: TokenKind.SIDE,
            # general
            kw.COLOUR_TOKEN: TokenKind.COLOUR,
        }
        self._1char_tokens = {
            Symbol.LEFT_BRACKET: TokenKind.LEFT_BRACKET,
            Symbol.RIGHT_BRACKET: TokenKind.RIGHT_BRACKET,
            Symbol.COLON: TokenKind.COLON,
            Symbol.SEMICOLON: TokenKind.SEMICOLON,
            Symbol.EQUALS: TokenKind.EQUALS,
            Symbol.COMMA: TokenKind.COMMA,
            Symbol.DOT: TokenKind.DOT,
            Symbol.STAR: TokenKind.TOOL_ID_START,
            Symbol.UNDERSCORE: TokenKind.PROC_ID_START
        }
        self._deltas = {
            State.N1: {Symbol.NUMBER: State.N2, Symbol.MINUS: State.N3},
            State.N2: {Symbol.NUMBER: State.N2, Symbol.DOT: State.N4},
            State.N3: {Symbol.NUMBER: State.N2, Symbol.DOT: State.N4},
            State.N4: {Symbol.NUMBER: State.N5},
            State.N5: {Symbol.NUMBER: State.N5}
        }

        self._state = None
        self._token_value = []
        self._tlr = Transliterator(source_text)
        self._tlr.read_next()

    def read_next(self) -> Token:
        self._token_value = []
        self._skip_blanks()
        line = self._tlr.line
        pos = self._tlr.position
        if self._tlr.symbol in self._1char_tokens.keys():
            kind = self._1char_tokens[self._tlr.symbol]
            self._tlr.read_next()
        else:
            match self._tlr.symbol:
                case Symbol.NUMBER | Symbol.MINUS:
                    self._state = State.N1
                    kind = self._read_number()
                case Symbol.LETTER | Symbol.LATIN_LETTER:
                    kind = self._read_id_or_keyword()
                case Symbol.DOUBLE_QUOTE:
                    kind = self._read_string(Symbol.DOUBLE_QUOTE)
                case Symbol.EOT:
                    kind = TokenKind.EOT
                case _:
                    raise LexerError(f"Неожиданный символ: {self._tlr.char}")
        return Token(kind, ''.join(self._token_value), line, pos)

    def _skip_blanks(self) -> None:
        while self._tlr.symbol in self._skippable:
            self._tlr.read_next()

    def _read_id_or_keyword(self) -> TokenKind:
        while self._tlr.symbol in self._identifier_chars:
            self._token_value.append(self._tlr.char)
            self._tlr.read_next()
        value = ''.join(self._token_value)
        if value in self._keywords.keys():
            return self._keywords[value]
        return TokenKind.IDENTIFIER

    def _read_string(self, quote: Symbol) -> TokenKind:
        stop_symbols = [quote, Symbol.EOT]
        self._tlr.read_next()  # чтение открывающего символа
        while self._tlr.symbol not in stop_symbols:
            self._token_value.append(self._tlr.char)
            self._tlr.read_next()
        if self._tlr.symbol != quote:
            raise LexerError("Ожидался закрывающий символ")
        self._tlr.read_next()  # чтение закрывающего символа
        return TokenKind.STRING

    def _read_number(self) -> TokenKind:
        while self._tlr.symbol is Symbol.NUMBER or \
                self._tlr.symbol is Symbol.MINUS or \
                self._tlr.symbol is Symbol.DOT:
            self._transition()
        if self._state != State.N2 and self._state != State.N5:
            raise LexerError(f"Неожиданный символ: {self._tlr.char}")
        return TokenKind.NUMBER

    def _transition(self) -> None:
        sym = self._tlr.symbol
        if sym in self._deltas[self._state].keys():
            self._state = self._deltas[self._state][sym]
            self._token_value.append(self._tlr.char)
            self._tlr.read_next()
        else:
            raise LexerError(f"Неожиданный символ: {self._tlr.char}")
