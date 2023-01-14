import pytest

from redpoll.analyzer.lexical import Lexer, LexerError
from redpoll.analyzer.token import TokenKind

point_str = "(2, 2)"
line_str = "*о_1: прямая, (2, 2), (4, 4), rgb(128, 128, 128)"
area_str = "*з1: зона, состав=...( \n" + \
           "  *о_1 ;\n" + \
           "  дуга: (3, 3), радиус=1, от=0, до=180;\n" + \
           ");"


def test_first_token():
    lexer = Lexer(point_str)

    token = lexer.read_next()

    assert token.line == 1
    assert token.position == 1
    assert token.kind == TokenKind.LEFT_BRACKET


def test_keyword_token():
    lexer = Lexer(line_str)

    token = None
    for i in range(4):
        token = lexer.read_next()

    assert token.line == 1
    assert token.position == 7
    assert token.kind == TokenKind.SEGMENT


def test_colour_token():
    lexer = Lexer(line_str)

    token = None
    for i in range(18):
        token = lexer.read_next()

    assert token.kind == TokenKind.COLOUR
    assert token.line == 1
    assert token.position == 31


def test_eot_token():
    lexer = Lexer(point_str)

    token = None
    for i in range(6):
        token = lexer.read_next()

    assert token.kind == TokenKind.EOT
    assert token.line == 1
    assert token.position == 7


def test_composite_token():
    lexer = Lexer(area_str)

    tokens = []
    token = lexer.read_next()
    tokens.append(token)
    while token.kind != TokenKind.EOT:
        token = lexer.read_next()
        tokens.append(token)

    assert tokens[3].kind == TokenKind.AREA
    assert tokens[3].line == 1
    assert tokens[-1].kind == TokenKind.EOT
    assert tokens[-1].line == 4
    assert tokens[-1].position == 3


def test_raise_on_invalid_token():
    lexer = Lexer("(2, #)")
    for i in range(3):
        _ = lexer.read_next()

    with pytest.raises(LexerError):
        _ = lexer.read_next()


def test_empty():
    lexer = Lexer("")
    token = lexer.read_next()
    assert token.kind == TokenKind.EOT


def test_raise_on_invalid_number():
    lexer = Lexer("-a")
    with pytest.raises(LexerError) as err:
        _ = lexer.read_next()
    assert "Неожиданный символ" in str(err.value)
