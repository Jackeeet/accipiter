from redpoll.expressions import *
from redpoll.types import OpType, DataType
from redpoll.resources import keywords as kw
from redpoll.resources.messages import parseerrors as err
from redpoll.analyzer.token import Token, TokenKind
from redpoll.analyzer.lexical import Lexer
from redpoll.analyzer.syntactic.parseerror import ParseError


class Parser:
    def __init__(self, input_str: str) -> None:
        self._complex_tool_types = {
            TokenKind.SEGMENT: DataType.SEGMENT,
            TokenKind.CURVE: DataType.CURVE,
            TokenKind.AREA: DataType.AREA,
            TokenKind.LINE: DataType.LINE,
            TokenKind.COUNTER: DataType.COUNTER
        }

        self._value_firsts = {TokenKind.TOOL_ID_START, TokenKind.DOT,
                              TokenKind.LEFT_BRACKET, TokenKind.COLOUR,
                              TokenKind.NUMBER, TokenKind.STRING, TokenKind.IDENTIFIER}

        self._lexer = Lexer(input_str)
        self._next_token()

    def parse(self) -> ProgramExpr | None:
        if self._token.kind == TokenKind.EOT:
            return None

        program = ProgramExpr()
        program.objects = self._parse_block(TokenKind.OBJECTS)
        program.tools = self._parse_block(TokenKind.TOOLS)
        program.processing = self._parse_block(TokenKind.PROCESSING)

        if self._token.kind != TokenKind.EOT:
            raise ParseError(err.extra_symbols())
        return program

    # noinspection PyTypeChecker
    def _parse_block(self, block_kind: TokenKind) -> BlockExpr:
        self._match(block_kind)
        self._match(TokenKind.COLON)
        match block_kind:
            case TokenKind.OBJECTS:
                block = ObjectBlockExpr()
                self._parse_object_list(block.items)
            case TokenKind.TOOLS:
                block = ToolBlockExpr()
                self._parse_tool_list(block.items)
            case TokenKind.PROCESSING:
                block = ProcessingBlockExpr()
                self._parse_processing_list(block.items)
            case _:
                raise ParseError(err.unsupported_block(block_kind))
        self._match(TokenKind.SEMICOLON)
        return block

    def _parse_object_list(self, objects: list[ObjectExpr]) -> None:
        while self._token.kind == TokenKind.IDENTIFIER:
            objects.append(self._parse_object_declaration())

    def _parse_object_declaration(self) -> ObjectExpr:
        obj = ObjectExpr(self._parse_object_id())
        self._match(TokenKind.SEMICOLON)
        return obj

    def _parse_object_id(self):
        return ObjectIdExpr(self._read_value(TokenKind.IDENTIFIER))

    def _parse_tool_list(self, tool_list: list[ToolExpr]) -> None:
        while self._token.kind == TokenKind.TOOL_ID_START:
            tool_list.append(self._parse_tool_declaration())

    def _parse_tool_declaration(self) -> ToolExpr:
        tool_id = self._parse_tool_id()
        self._match(TokenKind.COLON)
        expr = self._parse_tool()
        expr.id = tool_id
        self._match(TokenKind.SEMICOLON)
        return expr

    def _parse_tool(self) -> ToolExpr:
        expr = self._parse_type()
        params = dict()
        self._parse_named_params(params)
        for (name, value) in params.items():
            expr.params[name] = value
        return expr

    def _parse_tool_id(self) -> ToolIdExpr:
        self._match(TokenKind.TOOL_ID_START)
        return ToolIdExpr(self._read_value(TokenKind.IDENTIFIER))

    def _parse_type(self) -> ToolExpr:
        if self._token.kind == TokenKind.LEFT_BRACKET:
            coords = self._parse_coordinates()
            expr = PointExpr()
            expr.params[kw.POINT] = CoordsExpr((coords.value[0], coords.value[1]))
            return expr

        if self._token.kind in self._complex_tool_types:
            expr = ToolExpr.instantiate_with_type(self._complex_tool_types[self._token.kind])
            expr.params[kw.COLOUR] = ColourExpr((0, 0, 0))
            expr.params[kw.THICKNESS] = IntExpr(1)
            self._next_token()
            return expr

        raise ParseError(err.unexpected_token(self._token, "Тип инструмента"))

    def _parse_named_params(self, params: dict[str, ParamsExpr]) -> None:
        while self._token.kind == TokenKind.COMMA:
            self._match(TokenKind.COMMA)
            self._parse_named_param(params)

    def _parse_named_param(self, params: dict[str, ParamsExpr]) -> None:
        if self._token.kind == TokenKind.PARAM_NAME:
            name = self._read_value(TokenKind.PARAM_NAME)
            self._match(TokenKind.EQUALS)
            if name in params:
                raise ParseError(err.duplicated_param(name))
            params[name] = self._parse_value()
        else:
            raise ParseError(err.unexpected_token(self._token, "Параметр инструмента"))

    def _parse_value(self) -> ParamsExpr:
        match self._token.kind:
            case TokenKind.IDENTIFIER:
                return self._parse_object_id()
            case TokenKind.TOOL_ID_START:
                return self._parse_tool_id()
            case TokenKind.DOT:
                return self._parse_tool_parts()
            case TokenKind.LEFT_BRACKET:
                return self._parse_coordinates()
            case TokenKind.COLOUR:
                return self._parse_colour()
            case TokenKind.NUMBER | TokenKind.STRING:
                return self._parse_literal()
            case _:
                raise ParseError(err.unexpected_token(self._token, "Значение параметра"))

    def _parse_tool_parts(self) -> ToolPartsExpr:
        parts: list[ToolExpr | ToolIdExpr] = []
        for i in range(3):
            self._match(TokenKind.DOT)
        self._match(TokenKind.LEFT_BRACKET)
        parts.append(self._parse_tool_part())
        self._parse_next_parts(parts)
        self._match(TokenKind.RIGHT_BRACKET)
        return ToolPartsExpr(parts)

    def _parse_tool_part(self) -> ToolExpr | ToolIdExpr:
        match self._token.kind:
            case TokenKind.TOOL_ID_START:
                return self._parse_tool_id()
            case TokenKind.SEGMENT | TokenKind.CURVE | TokenKind.AREA | TokenKind.LINE | TokenKind.COUNTER:
                return self._parse_tool()
            case _:
                raise ParseError(err.unexpected_token(self._token, "Часть составного инструмента"))

    def _parse_next_parts(self, parts: list[ToolExpr | ToolIdExpr]) -> None:
        while self._token.kind == TokenKind.SEMICOLON:
            self._match(TokenKind.SEMICOLON)
            parts.append(self._parse_tool_part())

    def _parse_processing_list(self, rules: list[ProcessingExpr]) -> None:
        while True:
            if self._token.kind == TokenKind.PROC_ID_START:
                rules.append(self._parse_processing_declaration())
            elif self._token.kind == TokenKind.IF:
                rules.append(self._parse_condition())
            else:
                break

    def _parse_processing_id(self) -> ProcessingIdExpr:
        self._match(TokenKind.PROC_ID_START)
        return ProcessingIdExpr(self._read_value(TokenKind.IDENTIFIER))

    def _parse_processing_declaration(self) -> DeclarationExpr:
        expr = DeclarationExpr()
        expr.name = self._parse_processing_id()
        self._match(TokenKind.COLON)
        expr.body = self._parse_processing_decl_body()
        self._match(TokenKind.SEMICOLON)
        return expr

    def _parse_processing_decl_body(self) -> DeclarableExpr:
        match self._token.kind:
            case TokenKind.ACTION_NAME:
                return self._parse_action()
            case TokenKind.LEFT_BRACKET | TokenKind.IDENTIFIER | TokenKind.TOOL_ID_START | TokenKind.PROC_ID_START:
                return self._parse_event_disjunction()
            case _:
                raise ParseError(err.unsupported_processing_type())

    def _parse_action(self) -> ActionExpr:
        expr = ActionExpr()
        expr.name = ActionNameExpr(self._read_value(TokenKind.ACTION_NAME))
        self._match(TokenKind.LEFT_BRACKET)
        self._parse_params(expr.args)
        self._match(TokenKind.RIGHT_BRACKET)
        return expr

    def _parse_event_disjunction(self) -> BinaryExpr | EventExpr | ProcessingIdExpr:
        left = self._parse_event_conjunction()
        while self._token.kind == TokenKind.OR:
            self._match(TokenKind.OR)
            right = self._parse_event_conjunction()
            left = BinaryExpr(left, OpType.OR, right)
        return left

    def _parse_event_conjunction(self) -> BinaryExpr | EventExpr | ProcessingIdExpr:
        left = self._parse_event_or_event_id()
        while self._token.kind == TokenKind.AND:
            self._match(TokenKind.AND)
            right = self._parse_event_or_event_id()
            left = BinaryExpr(left, OpType.AND, right)
        return left

    def _parse_event_or_event_id(self) -> BinaryExpr | EventExpr | ProcessingIdExpr:
        match self._token.kind:
            case TokenKind.PROC_ID_START:
                return self._parse_processing_id()
            case TokenKind.IDENTIFIER | TokenKind.TOOL_ID_START:
                return self._parse_event()
            case TokenKind.LEFT_BRACKET:
                self._match(TokenKind.LEFT_BRACKET)
                event = self._parse_event_disjunction()
                self._match(TokenKind.RIGHT_BRACKET)
                return event
            case _:
                raise ParseError(err.unexpected_token(self._token, "Событие"))

    def _parse_event(self) -> EventExpr:
        expr = EventExpr()
        if self._token.kind == TokenKind.IDENTIFIER:
            expr.target = ObjectIdExpr(self._read_value(TokenKind.IDENTIFIER))
        elif self._token.kind == TokenKind.TOOL_ID_START:
            expr.target = self._parse_tool_id()
        else:
            raise ParseError(err.unexpected_token(self._token, "Источник события"))

        self._match(TokenKind.DOT)
        expr.name = EventNameExpr(self._read_value(TokenKind.EVENT_NAME))
        self._match(TokenKind.LEFT_BRACKET)
        self._parse_params(expr.args)
        self._match(TokenKind.RIGHT_BRACKET)
        return expr

    def _parse_params(self, param_list: list[ParamsExpr]) -> None:
        if self._token.kind in self._value_firsts:
            param_list.append(self._parse_value())
            self._parse_next_params(param_list)

    def _parse_next_params(self, param_list: list[ParamsExpr]) -> None:
        while self._token.kind == TokenKind.COMMA:
            self._match(TokenKind.COMMA)
            param_list.append(self._parse_value())

    def _parse_condition(self) -> ConditionExpr:
        expr = ConditionExpr()
        self._match(TokenKind.IF)
        expr.event = self._parse_event_disjunction()
        self._match(TokenKind.COLON)
        self._parse_condition_actions(expr.actions)
        self._match(TokenKind.SEMICOLON)
        return expr

    def _parse_condition_actions(self, action_list: list[ProcessingIdExpr | ActionExpr]) -> None:
        while self._token.kind == TokenKind.PROC_ID_START or self._token.kind == TokenKind.ACTION_NAME:
            if self._token.kind == TokenKind.PROC_ID_START:
                action_list.append(self._parse_processing_id())
            elif self._token.kind == TokenKind.ACTION_NAME:
                action_list.append(self._parse_action())
            self._match(TokenKind.SEMICOLON)

    def _parse_literal(self) -> AtomicExpr:
        match self._token.kind:
            case TokenKind.NUMBER:
                return IntExpr(int(self._read_value(TokenKind.NUMBER)))
            case TokenKind.STRING:
                return StringExpr(self._read_value(TokenKind.STRING))
            case _:
                raise ParseError(err.unexpected_token(self._token, "Литерал"))

    def _parse_colour(self) -> AtomicExpr:
        self._match(TokenKind.COLOUR)
        # noinspection DuplicatedCode
        self._match(TokenKind.LEFT_BRACKET)
        r = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.COMMA)
        g = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.COMMA)
        b = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.RIGHT_BRACKET)
        return ColourExpr((r, g, b))

    def _parse_coordinates(self) -> AtomicExpr:
        # noinspection DuplicatedCode
        self._match(TokenKind.LEFT_BRACKET)
        x = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.COMMA)
        y = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.RIGHT_BRACKET)
        return CoordsExpr((x, y))

    def _read_token(self, kind: TokenKind) -> Token:
        """Возвращает текущий токен, если его тип совпадает с указанным,
        и читает следующий токен.

        :param kind: тип текущего токена
        :return: текущий токен
        """
        token = self._token
        if token.kind != kind:
            raise ParseError(err.unexpected_token(token, "read_token"))
        self._next_token()
        return token

    def _read_value(self, kind: TokenKind) -> str:
        """Возвращает значение текущего токена, если его тип совпадает с указанным,
        и читает следующий токен.

        :param kind: тип текущего токена
        :return: значение текущего токена
        """
        if self._token.kind != kind:
            raise ParseError(err.unexpected_token(self._token, "read_value"))
        value = self._token.value
        self._next_token()
        return value

    def _match(self, kind: TokenKind) -> None:
        """Читает следующий токен, если тип текущего токена совпадает с указанным.

        :param kind: тип токена
        """
        if self._token.kind != kind:
            raise ParseError(err.unexpected_token(self._token, "match"))
        self._next_token()

    def _next_token(self) -> None:
        self._token = self._lexer.read_next()
