import pytest

from redpoll.analyzer.syntactic import ParseError, Parser
from redpoll.expressions import ObjectExpr, ObjectIdExpr
from redpoll.expressions.programexpr import ProgramExpr
from redpoll.resources.messages import parseerrors as err


def test_parse_empty():
    parser = Parser("")
    expr = parser.parse()
    assert expr is None


def test_parse_empty_blocks():
    parser = Parser("объекты: ; инструменты: ; обработка: ;")

    expr: ProgramExpr = parser.parse()

    assert type(expr) is ProgramExpr
    assert len(expr.objects.items) == 0
    assert len(expr.tools.items) == 0
    assert len(expr.processing.items) == 0


def test_parse_single_object_block():
    parser = Parser("объекты: человек; ; инструменты: ; обработка: ;")

    expr: ProgramExpr = parser.parse()

    assert type(expr) is ProgramExpr

    items: list[ObjectExpr] = expr.objects.items
    assert len(items) == 1
    assert type(items[0]) is ObjectExpr
    assert type(items[0].id) is ObjectIdExpr
    assert items[0].id.value == "человек"


def test_parse_multiple_objects_block():
    parser = Parser("объекты: человек; автомобиль; ; инструменты: ; обработка: ;")

    expr: ProgramExpr = parser.parse()

    assert type(expr) is ProgramExpr

    items: list[ObjectExpr] = expr.objects.items
    assert len(items) == 2
    assert type(items[1]) is ObjectExpr
    assert items[1].id.value == "автомобиль"


def test_raise_on_extra_tokens():
    parser = Parser("объекты: ; инструменты: ; обработка: ; (0,0): т1")
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert err.extra_symbols() in str(error.value)
