from redpoll.analyzer.lexical import Lexer
from redpoll.analyzer.syntactic.parseerror import ParseError
from redpoll.analyzer.token import Token, TokenKind
from redpoll.expressions import *
from redpoll.resources import keywords as kw
from redpoll.resources.lookup import action, event
from redpoll.resources.messages import parseerrors as err
from redpoll.types import DataType, OpType


class Parser:
    _param_lists: dict[str, list[str]]

    def __init__(self, input_str: str) -> None:
        self._complex_tool_types = {
            TokenKind.SEGMENT: DataType.SEGMENT,
            TokenKind.ARC: DataType.ARC,
            TokenKind.AREA: DataType.AREA,
            TokenKind.LINE: DataType.LINE,
            TokenKind.COUNTER: DataType.COUNTER
        }

        self._simple_value_firsts = {TokenKind.TOOL_ID_START, TokenKind.DOT, TokenKind.TRIPLE_DOT,
                                     TokenKind.LEFT_BRACKET, TokenKind.COLOUR, TokenKind.SIDE,
                                     TokenKind.NUMBER, TokenKind.STRING, TokenKind.IDENTIFIER}
        self._param_lists = {**action.param_lists, **event.param_lists}

        self._lexer = Lexer(input_str)
        self._next_token()

    def parse(self) -> ProgramExpr | None:
        if self._token.kind == TokenKind.EOT:
            return None

        program = ProgramExpr(*self._expr_position)
        program.objects = self._parse_block(TokenKind.OBJECTS)
        program.tools = self._parse_block(TokenKind.TOOLS)
        program.processing = self._parse_block(TokenKind.PROCESSING)

        if self._token.kind != TokenKind.EOT:
            raise ParseError(self._token, err.extra_symbols())
        return program

    # noinspection PyTypeChecker
    def _parse_block(self, block_kind: TokenKind) -> BlockExpr:
        self._match(block_kind)
        self._match(TokenKind.COLON)
        match block_kind:
            case TokenKind.OBJECTS:
                block = ObjectBlockExpr(*self._expr_position)
                self._parse_object_list(block.items)
            case TokenKind.TOOLS:
                block = ToolBlockExpr(*self._expr_position)
                self._parse_tool_list(block.items)
            case TokenKind.PROCESSING:
                block = ProcessingBlockExpr(*self._expr_position)
                self._parse_processing_list(block.items)
            case _:
                raise ParseError(self._token, err.unsupported_block(block_kind))
        self._match(TokenKind.SEMICOLON)
        return block

    def _parse_object_list(self, objects: list[ObjectExpr]) -> None:
        while self._token.kind == TokenKind.IDENTIFIER:
            objects.append(self._parse_object_declaration())

    def _parse_object_declaration(self) -> ObjectExpr:
        obj = ObjectExpr(*self._expr_position, self._parse_object_id())
        self._match(TokenKind.SEMICOLON)
        return obj

    def _parse_object_id(self):
        return ObjectIdExpr(*self._expr_position, self._read_value(TokenKind.IDENTIFIER))

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
        return ToolIdExpr(*self._expr_position, self._read_value(TokenKind.IDENTIFIER))

    def _parse_type(self) -> ToolExpr:
        if self._token.kind == TokenKind.DOT:
            coords = self._parse_coordinates()
            expr = PointExpr(*self._expr_position)
            expr.params[kw.POINT] = CoordsExpr(*self._expr_position, (coords.value[0], coords.value[1]))
            return expr

        if self._token.kind in self._complex_tool_types:
            expr = instantiate_tool_with_type(
                self._complex_tool_types[self._token.kind],
                *self._expr_position
            )
            expr.params[kw.COLOUR] = ColourExpr(*self._expr_position, (0, 0, 0))
            expr.params[kw.THICKNESS] = IntExpr(*self._expr_position, 1)
            self._next_token()
            return expr

        raise ParseError(self._token, err.unexpected_token(self._token, "Тип инструмента"))

    def _parse_named_params(self, params: dict[str, ParamsExpr]) -> None:
        while self._token.kind == TokenKind.COMMA:
            self._match(TokenKind.COMMA)
            self._parse_named_param(params)

    def _parse_named_param(self, params: dict[str, ParamsExpr]) -> None:
        if self._token.kind == TokenKind.PARAM_NAME:
            name = self._read_value(TokenKind.PARAM_NAME)
            self._match(TokenKind.EQUALS)
            if name in params:
                raise ParseError(self._token, err.duplicated_param(name))
            params[name] = self._parse_value()
        else:
            raise ParseError(self._token, err.unexpected_token(self._token, "Параметр инструмента"))

    def _parse_value(self) -> ParamsExpr:
        match self._token.kind:
            case TokenKind.IDENTIFIER:
                return self._parse_object_id()
            case TokenKind.TOOL_ID_START:
                return self._parse_tool_id()
            case TokenKind.TRIPLE_DOT:
                return self._parse_tool_parts()
            case TokenKind.DOT:
                return self._parse_coordinates()
            case TokenKind.COLOUR:
                return self._parse_colour()
            case TokenKind.NUMBER | TokenKind.STRING:
                return self._parse_literal()
            case TokenKind.SIDE:
                return self._parse_side()
            case TokenKind.LEFT_BRACKET:
                self._match(TokenKind.LEFT_BRACKET)
                value = self._parse_value_disjunction()
                self._match(TokenKind.RIGHT_BRACKET)
                return value
            case _:
                raise ParseError(self._token, err.unexpected_token(self._token, "Значение параметра"))

    def _parse_value_disjunction(self) -> BinaryExpr | ParamsExpr:
        left = self._parse_value_conjunction()
        while self._token.kind == TokenKind.OR:
            self._match(TokenKind.OR)
            right = self._parse_value_conjunction()
            left = BinaryExpr(*self._expr_position, left, OpType.OR, right)
        return left

    def _parse_value_conjunction(self) -> BinaryExpr | ParamsExpr:
        left = self._parse_value()
        while self._token.kind == TokenKind.AND:
            self._match(TokenKind.AND)
            right = self._parse_value()
            left = BinaryExpr(*self._expr_position, left, OpType.AND, right)
        return left

    def _parse_tool_parts(self) -> ToolPartsExpr:
        self._match(TokenKind.TRIPLE_DOT)
        self._match(TokenKind.LEFT_BRACKET)
        parts: list[ToolExpr | ToolIdExpr] = [self._parse_tool_part()]
        while self._token.kind == TokenKind.SEMICOLON:
            self._match(TokenKind.SEMICOLON)
            parts.append(self._parse_tool_part())
        self._match(TokenKind.RIGHT_BRACKET)
        return ToolPartsExpr(*self._expr_position, parts)

    def _parse_tool_part(self) -> ToolExpr | ToolIdExpr:
        match self._token.kind:
            case TokenKind.TOOL_ID_START:
                return self._parse_tool_id()
            case TokenKind.SEGMENT | TokenKind.ARC | TokenKind.AREA | TokenKind.LINE | TokenKind.COUNTER:
                return self._parse_tool()
            case _:
                raise ParseError(self._token, err.unexpected_token(self._token, "Часть составного инструмента"))

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
        return ProcessingIdExpr(*self._expr_position, self._read_value(TokenKind.IDENTIFIER))

    def _parse_processing_declaration(self) -> DeclarationExpr:
        expr = DeclarationExpr(*self._expr_position)
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
                raise ParseError(self._token, err.unsupported_processing_type())

    def _parse_action(self) -> ActionExpr:
        expr = ActionExpr(*self._expr_position)
        expr.name = ActionNameExpr(*self._expr_position, self._read_value(TokenKind.ACTION_NAME))
        self._match(TokenKind.LEFT_BRACKET)
        self._parse_args(expr.args, expr.name.value)
        self._match(TokenKind.RIGHT_BRACKET)
        return expr

    def _parse_event_disjunction(self) -> BinaryExpr | EventExpr | ProcessingIdExpr:
        left = self._parse_event_conjunction()
        while self._token.kind == TokenKind.OR:
            self._match(TokenKind.OR)
            right = self._parse_event_conjunction()
            left = BinaryExpr(*self._expr_position, left, OpType.OR, right)
        return left

    def _parse_event_conjunction(self) -> BinaryExpr | EventExpr | ProcessingIdExpr:
        left = self._parse_event_or_event_id()
        while self._token.kind == TokenKind.AND:
            self._match(TokenKind.AND)
            right = self._parse_event_or_event_id()
            left = BinaryExpr(*self._expr_position, left, OpType.AND, right)
        return left

    def _parse_event_or_event_id(self) -> BinaryExpr | EventExpr | ProcessingIdExpr:
        match self._token.kind:
            case TokenKind.PROC_ID_START:
                return self._parse_processing_id()
            case TokenKind.IDENTIFIER | TokenKind.TOOL_ID_START:
                return self._parse_event()
            case TokenKind.LEFT_BRACKET:
                self._match(TokenKind.LEFT_BRACKET)
                evt = self._parse_event_disjunction()
                self._match(TokenKind.RIGHT_BRACKET)
                return evt
            case _:
                raise ParseError(self._token, err.unexpected_token(self._token, "Событие"))

    def _parse_event(self) -> EventExpr:
        expr = EventExpr(*self._expr_position)
        if self._token.kind == TokenKind.IDENTIFIER:
            expr.target = ObjectIdExpr(*self._expr_position, self._read_value(TokenKind.IDENTIFIER))
        elif self._token.kind == TokenKind.TOOL_ID_START:
            expr.target = self._parse_tool_id()
        else:
            raise ParseError(self._token, err.unexpected_token(self._token, "Источник события"))

        self._match(TokenKind.DOT)
        expr.name = EventNameExpr(*self._expr_position, self._read_value(TokenKind.EVENT_NAME))
        self._match(TokenKind.LEFT_BRACKET)
        self._parse_args(expr.args, expr.name.value)
        self._match(TokenKind.RIGHT_BRACKET)
        return expr

    def _parse_args(self, args: dict[str, ParamsExpr], decl_name: str) -> None:
        if self._token.kind in self._simple_value_firsts:
            arg_index = 0
            param_names = self._param_lists[decl_name]
            args[param_names[arg_index]] = self._parse_value()
            while self._token.kind == TokenKind.COMMA:
                self._match(TokenKind.COMMA)
                arg_index += 1
                args[param_names[arg_index]] = self._parse_value()

    def _parse_condition(self) -> ConditionExpr:
        expr = ConditionExpr(*self._expr_position)
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
                return IntExpr(*self._expr_position, int(self._read_value(TokenKind.NUMBER)))
            case TokenKind.STRING:
                return StringExpr(*self._expr_position, self._read_value(TokenKind.STRING))
            case _:
                raise ParseError(self._token, err.unexpected_token(self._token, "Литерал"))

    def _parse_colour(self) -> AtomicExpr:
        self._match(TokenKind.COLOUR)
        self._match(TokenKind.LEFT_BRACKET)
        r = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.COMMA)
        g = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.COMMA)
        b = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.RIGHT_BRACKET)
        return ColourExpr(*self._expr_position, (r, g, b))

    def _parse_coordinates(self) -> AtomicExpr:
        self._match(TokenKind.DOT)
        self._match(TokenKind.LEFT_BRACKET)
        x = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.COMMA)
        y = int(self._read_value(TokenKind.NUMBER))
        self._match(TokenKind.RIGHT_BRACKET)
        return CoordsExpr(*self._expr_position, (x, y))

    def _parse_side(self) -> SideExpr:
        if self._token.kind == TokenKind.SIDE:
            return SideExpr(*self._expr_position, self._read_token(TokenKind.SIDE))
        raise ParseError(self._token, err.unexpected_token(self._token, "Сторона"))

    def _read_token(self, kind: TokenKind) -> Token:
        """Возвращает текущий токен, если его тип совпадает с указанным,
        и читает следующий токен.

        :param kind: Тип текущего токена
        :return: текущий токен
        """
        token = self._token
        if token.kind != kind:
            raise ParseError(self._token, err.unexpected_token(token, "read_token"))
        self._next_token()
        return token

    def _read_value(self, kind: TokenKind) -> str:
        """Возвращает значение текущего токена, если его тип совпадает с указанным,
        и читает следующий токен.

        :param kind: Тип текущего токена
        :return: значение текущего токена
        """
        if self._token.kind != kind:
            raise ParseError(self._token, err.unexpected_token(self._token, "read_value"))
        value = self._token.value
        self._next_token()
        return value

    def _match(self, kind: TokenKind) -> None:
        """Читает следующий токен, если тип текущего токена совпадает с указанным.

        :param kind: Тип токена
        """
        if self._token.kind != kind:
            raise ParseError(self._token, err.unexpected_token(self._token, "match"))
        self._next_token()

    def _next_token(self) -> None:
        self._token = self._lexer.read_next()

    @property
    def _expr_position(self) -> tuple[int, int]:
        return self._token.line, self._token.position
