import pytest

from redpoll.types import DataType
from redpoll.analyzer.syntactic import Parser
from redpoll.expressions import *
from redpoll.types import OpType


@pytest.fixture
def prefix():
    return "объекты: ; инструменты: ; обработка: "


@pytest.fixture
def suffix():
    return " ;"


def test_parse_event_declaration(prefix, suffix):
    declaration = "_пр1: человек.пересекает(элемент=*л1);"
    parser = Parser(prefix + declaration + suffix)

    program: ProgramExpr = parser.parse()

    assert len(program.processing.items) == 1
    expr: DeclarationExpr = program.processing.items[0]

    assert type(expr) is DeclarationExpr
    assert type(expr.name) is ProcessingIdExpr
    assert expr.name.value == "пр1"

    event: EventExpr = expr.body
    assert type(event) is EventExpr
    assert type(event.target) is ObjectIdExpr
    assert event.target.value == "человек"
    assert type(event.name) is EventIdExpr
    assert event.name.value == "пересекает"

    params: list[ParamsExpr] = event.params
    assert len(params) == 1
    assert type(params['элемент']) is ToolIdExpr
    assert params['элемент'].value == "л1"


def test_parse_chain_event_decl(prefix, suffix):
    declaration = "_пр1: человек.пересекает(элемент=*л1) или человек.пересекает(элемент=*л2) и\n" + \
                  "_событие1 или (человек.пересекает(элемент=*л4)) и\n" + \
                  "человек.покидает(элемент=*зона1) и человек.пересекает(элемент=*л5);"
    parser = Parser(prefix + declaration + suffix)

    program: ProgramExpr = parser.parse()

    expr: DeclarationExpr = program.processing.items[0]
    assert type(expr) is DeclarationExpr

    body: BinaryExpr = expr.body
    assert type(body) is BinaryExpr
    assert body.op == OpType.OR
    assert type(body.left) is BinaryExpr
    assert type(body.right) is BinaryExpr

    left = body.left
    assert left.op == OpType.OR
    assert type(left.left) is EventExpr
    assert left.left.target.value == "человек"
    assert type(left.right) is BinaryExpr
    assert left.right.op == OpType.AND
    assert type(left.right.left) is EventExpr
    assert type(left.right.right) is ProcessingIdExpr

    right = body.right
    assert right.op == OpType.AND
    assert type(right.left) is BinaryExpr
    assert right.left.op == OpType.AND
    assert right.left.right.name.value == "покидает"
    assert type(right.right) is EventExpr


def test_parse_grouped_chain_decl(prefix, suffix):
    declaration = "_пр1: (человек.пересекает(элемент=*л1) или человек.пересекает(элемент=*л2)) и\n" + \
                  "(человек.пересекает(элемент=*л3) или человек.пересекает(элемент=*л4));"
    parser = Parser(prefix + declaration + suffix)

    program: ProgramExpr = parser.parse()
    expr: DeclarationExpr = program.processing.items[0]

    body: BinaryExpr = expr.body
    assert body.op == OpType.AND
    assert body.left.op == OpType.OR
    assert type(body.left.left) is EventExpr
    assert type(body.left.right) is EventExpr
    assert body.right.op == OpType.OR
    assert type(body.right.left) is EventExpr
    assert type(body.right.right) is EventExpr


def test_parse_tool_event_declaration(prefix, suffix):
    declaration = "_а: *сч1.равен(число=1000);"
    parser = Parser(prefix + declaration + suffix)

    program: ProgramExpr = parser.parse()
    expr: DeclarationExpr = program.processing.items[0]

    body: EventExpr = expr.body
    assert type(body.target) is ToolIdExpr
    assert body.target.value == "сч1"
    assert body.name.value == "равен"
    assert len(body.params) == 1
    assert body.params['число'] == AtomicExpr(1000, DataType.INT)


def test_parse_action_declaration(prefix, suffix):
    declaration = "_действие1: оповестить(сообщение=\"сообщение 1\");"
    parser = Parser(prefix + declaration + suffix)

    program: ProgramExpr = parser.parse()
    expr: DeclarationExpr = program.processing.items[0]

    assert type(expr.name) is ProcessingIdExpr
    assert expr.name.value == "действие1"

    body: ActionExpr = expr.body
    assert type(body) is ActionExpr
    assert type(body.name) is ActionIdExpr
    assert body.name.value == "оповестить"
    assert len(body.params) == 1
    assert body.params['сообщение'] == AtomicExpr("сообщение 1", DataType.STRING)


def test_parse_parameterless_action_declaration(prefix, suffix):
    declaration = "_действие1: сохранить();"
    parser = Parser(prefix + declaration + suffix)

    program: ProgramExpr = parser.parse()
    expr: DeclarationExpr = program.processing.items[0]

    assert type(expr.name) is ProcessingIdExpr
    assert expr.name.value == "действие1"

    body: ActionExpr = expr.body
    assert type(body) is ActionExpr
    assert type(body.name) is ActionIdExpr
    assert body.name.value == "сохранить"
    assert len(body.params) == 0


def test_parse_id_condition(prefix, suffix):
    check = "если _событие1: _действие1; ;"
    parser = Parser(prefix + check + suffix)

    program: ProgramExpr = parser.parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: ProcessingIdExpr = expr.event
    assert type(event) is ProcessingIdExpr
    assert event.value == "событие1"

    actions: list[ActionExpr | ProcessingIdExpr] = expr.actions
    assert len(actions) == 1
    assert type(actions[0]) is ProcessingIdExpr
    assert actions[0].value == "действие1"


def test_parse_event_condition(prefix, suffix):
    check = "если (автомобиль.пересекает(элемент=*л2)):\n" + \
            "    _действие1;\n" + \
            "    оповестить(сообщение=\"сообщение\");\n" + \
            ";"
    parser = Parser(prefix + check + suffix)

    program: ProgramExpr = parser.parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: EventExpr = expr.event
    assert type(event) is EventExpr
    assert event.target.value == "автомобиль"
    assert event.name.value == "пересекает"

    actions: list[ActionExpr | ProcessingIdExpr] = expr.actions
    assert len(actions) == 2
    assert type(actions[0]) is ProcessingIdExpr
    assert actions[0].value == "действие1"
    assert type(actions[1]) is ActionExpr
    assert actions[1].name.value == "оповестить"
    msg: AtomicExpr = actions[1].params["сообщение"]
    assert type(msg) is AtomicExpr and msg.type == DataType.STRING
    assert msg.value == "'сообщение'"


def test_parse_double_id_condition(prefix, suffix):
    check = "если _событие1 или _событие2: ;"
    parser = Parser(prefix + check + suffix)

    program: ProgramExpr = parser.parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr
    assert event.op == OpType.OR
    assert type(event.left) is ProcessingIdExpr
    assert type(event.right) is ProcessingIdExpr


def test_parse_double_event_condition(prefix, suffix):
    check = "если (автомобиль.пересекает(элемент=*л1)) и (автомобиль.пересекает(элемент=*л2)): ;"
    parser = Parser(prefix + check + suffix)

    program: ProgramExpr = parser.parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr
    assert event.op == OpType.AND
    assert type(event.left) is EventExpr
    assert type(event.right) is EventExpr


def test_parse_id_event_condition(prefix, suffix):
    check = "если _событие1 и (автомобиль.пересекает(элемент=*л2)): ;"
    parser = Parser(prefix + check + suffix)

    program: ProgramExpr = parser.parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr
    assert type(event.left) is ProcessingIdExpr
    assert type(event.right) is EventExpr


def test_parse_event_id_condition(prefix, suffix):
    check = "если (автомобиль.пересекает(элемент=*л1)) и _событие2: ;"
    parser = Parser(prefix + check + suffix)

    program: ProgramExpr = parser.parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr
    assert type(event.left) is EventExpr
    assert type(event.right) is ProcessingIdExpr
