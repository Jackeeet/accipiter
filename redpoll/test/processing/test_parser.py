import pytest

from redpoll.analyzer.syntactic import Parser
from redpoll.expressions import *
from redpoll.types import OpType, Side
from redpoll.resources.lookup.params import ParamName as pn


@pytest.fixture
def prefix():
    return "объекты: ; инструменты: ; обработка: "


@pytest.fixture
def suffix():
    return " ;"


def test_parse_event_declaration(prefix, suffix):
    declaration = "_пр1: человек.пересекает(*л1);"

    program: ProgramExpr = Parser(prefix + declaration + suffix).parse()

    assert len(program.processing.items) == 1
    expr: DeclarationExpr = program.processing.items[0]

    assert type(expr) is DeclarationExpr \
           and type(expr.name) is ProcessingIdExpr \
           and expr.name.value == "пр1"

    event: EventExpr = expr.body
    assert type(event) is EventExpr \
           and type(event.target) is ObjectIdExpr \
           and type(event.name) is EventNameExpr

    assert event.target.value == "человек" and event.name.value == "пересекает"

    args: list[ParamsExpr] = event.args
    assert len(args) == 1 and pn.TOOLS in args

    tool_id: AtomicExpr = args[pn.TOOLS]
    assert type(tool_id) is ToolIdExpr and tool_id.value == "л1"


def test_parse_chain_event_decl(prefix, suffix):
    declaration = "_пр1: человек.пересекает(*л1) или человек.пересекает(*л2) и\n" + \
                  "_событие1 или (человек.пересекает(*л4)) и\n" + \
                  "человек.покидает(*зона1) и человек.пересекает(*л5);"

    program: ProgramExpr = Parser(prefix + declaration + suffix).parse()

    expr: DeclarationExpr = program.processing.items[0]
    assert type(expr) is DeclarationExpr

    body: BinaryExpr = expr.body
    assert type(body) is BinaryExpr \
           and body.op == OpType.OR \
           and type(body.left) is BinaryExpr \
           and type(body.right) is BinaryExpr

    left = body.left
    assert left.op == OpType.OR \
           and type(left.left) is EventExpr \
           and type(left.right) is BinaryExpr
    assert left.left.target.value == "человек"
    assert left.right.op == OpType.AND \
           and type(left.right.left) is EventExpr \
           and type(left.right.right) is ProcessingIdExpr

    right = body.right
    assert right.op == OpType.AND \
           and type(right.left) is BinaryExpr
    assert right.left.op == OpType.AND
    assert right.left.right.name.value == "покидает"
    assert type(right.right) is EventExpr


def test_parse_grouped_chain_decl(prefix, suffix):
    declaration = "_пр1: (человек.пересекает(*л1) или человек.пересекает(*л2)) и\n" + \
                  "(человек.пересекает(*л3) или человек.пересекает(*л4));"

    program: ProgramExpr = Parser(prefix + declaration + suffix).parse()
    expr: DeclarationExpr = program.processing.items[0]

    body: BinaryExpr = expr.body
    assert body.op == OpType.AND
    assert body.left.op == OpType.OR \
           and type(body.left.left) is EventExpr \
           and type(body.left.right) is EventExpr
    assert body.right.op == OpType.OR \
           and type(body.right.left) is EventExpr \
           and type(body.right.right) is EventExpr


def test_parse_tool_event_declaration(prefix, suffix):
    declaration = "_а: *сч1.равен(1000);"

    program: ProgramExpr = Parser(prefix + declaration + suffix).parse()
    expr: DeclarationExpr = program.processing.items[0]

    body: EventExpr = expr.body
    assert type(body.target) is ToolIdExpr \
           and body.target.value == "сч1"
    assert body.name.value == "равен"
    assert len(body.args) == 1 \
           and body.args[pn.NUMBER] == IntExpr(-1, -1, 1000)


def test_parse_action_declaration(prefix, suffix):
    declaration = "_действие1: оповестить(\"сообщение 1\");"

    program: ProgramExpr = Parser(prefix + declaration + suffix).parse()

    expr: DeclarationExpr = program.processing.items[0]
    assert type(expr.name) is ProcessingIdExpr and expr.name.value == "действие1"

    body: ActionExpr = expr.body
    assert type(body) is ActionExpr \
           and type(body.name) is ActionNameExpr \
           and body.name.value == "оповестить" \
           and len(body.args) == 1 \
           and body.args[pn.MESSAGE] == StringExpr(-1, -1, "сообщение 1")


def test_parse_parameterless_action_declaration(prefix, suffix):
    declaration = "_действие1: сохранить();"

    program: ProgramExpr = Parser(prefix + declaration + suffix).parse()
    expr: DeclarationExpr = program.processing.items[0]

    assert type(expr.name) is ProcessingIdExpr and expr.name.value == "действие1"

    body: ActionExpr = expr.body
    assert type(body) is ActionExpr \
           and type(body.name) is ActionNameExpr \
           and body.name.value == "сохранить" \
           and len(body.args) == 0


def test_parse_id_condition(prefix, suffix):
    check = "если _событие1: _действие1; ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: ProcessingIdExpr = expr.event
    assert type(event) is ProcessingIdExpr and event.value == "событие1"

    actions: list[ActionExpr | ProcessingIdExpr] = expr.actions
    assert len(actions) == 1 \
           and type(actions[0]) is ProcessingIdExpr \
           and actions[0].value == "действие1"


def test_parse_event_condition(prefix, suffix):
    check = "если (автомобиль.пересекает(*л2)):\n" + \
            "    _действие1;\n" + \
            "    оповестить(\"сообщение\");\n" + \
            ";"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: EventExpr = expr.event
    assert type(event) is EventExpr \
           and event.target.value == "автомобиль" \
           and event.name.value == "пересекает"

    actions: list[ActionExpr | ProcessingIdExpr] = expr.actions
    assert len(actions) == 2

    assert type(actions[0]) is ProcessingIdExpr and actions[0].value == "действие1"
    assert type(actions[1]) is ActionExpr and actions[1].name.value == "оповестить"

    msg: StringExpr = actions[1].args[pn.MESSAGE]
    assert type(msg) is StringExpr \
           and msg.type == DataType.STRING \
           and msg.value == "'сообщение'"


def test_parse_double_id_condition(prefix, suffix):
    check = "если _событие1 или _событие2: ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr \
           and event.op == OpType.OR \
           and type(event.left) is ProcessingIdExpr \
           and type(event.right) is ProcessingIdExpr


def test_parse_double_event_condition(prefix, suffix):
    check = "если (автомобиль.пересекает(*л1)) и (автомобиль.пересекает(*л2)): ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr \
           and event.op == OpType.AND \
           and type(event.left) is EventExpr \
           and type(event.right) is EventExpr


def test_parse_id_event_condition(prefix, suffix):
    check = "если _событие1 и (автомобиль.пересекает(*л2)): ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr \
           and type(event.left) is ProcessingIdExpr \
           and type(event.right) is EventExpr


def test_parse_event_id_condition(prefix, suffix):
    check = "если (автомобиль.пересекает(*л1)) и _событие2: ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    expr: ConditionExpr = program.processing.items[0]
    assert type(expr) is ConditionExpr

    event: BinaryExpr = expr.event
    assert type(event) is BinaryExpr \
           and type(event.left) is EventExpr \
           and type(event.right) is ProcessingIdExpr


def test_parse_single_crossing_side_param(prefix, suffix):
    check = "если (автомобиль.пересекает(*л1, слева)): ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    event: EventExpr = program.processing.items[0].event
    assert type(event) is EventExpr and len(event.args) == 2

    assert type(event.args[pn.TOOLS]) is ToolIdExpr

    side: AtomicExpr = event.args[pn.SIDES]
    assert type(side) is SideExpr and side.value == Side.LEFT


def test_parse_side_param_disjunction(prefix, suffix):
    check = "если (автомобиль.пересекает(*л1, (слева или сверху))): ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    event: EventExpr = program.processing.items[0].event
    assert type(event) is EventExpr and len(event.args) == 2

    sides: BinaryExpr = event.args[pn.SIDES]
    assert type(sides) is BinaryExpr and sides.op == OpType.OR \
           and type(sides.left) is SideExpr and sides.left.value == Side.LEFT \
           and type(sides.right) is SideExpr and sides.right.value == Side.TOP


def test_parse_side_param_conjunction(prefix, suffix):
    check = "если (автомобиль.пересекает(*л1, (справа и снизу))): ;"

    program: ProgramExpr = Parser(prefix + check + suffix).parse()

    event: EventExpr = program.processing.items[0].event
    assert type(event) is EventExpr and len(event.args) == 2

    sides: BinaryExpr = event.args[pn.SIDES]
    assert type(sides) is BinaryExpr and sides.op == OpType.AND \
           and type(sides.left) is SideExpr and sides.left.value == Side.RIGHT \
           and type(sides.right) is SideExpr and sides.right.value == Side.BOTTOM


def test_parse_side_operator_precedence(prefix, suffix):
    check = "если (автомобиль.пересекает(*л1, (справа и (снизу или сверху) или слева))): ;"

    event: EventExpr = Parser(prefix + check + suffix).parse().processing.items[0].event
    assert type(event) is EventExpr and len(event.args) == 2

    sides: BinaryExpr = event.args[pn.SIDES]
    assert type(sides) is BinaryExpr and sides.op == OpType.OR

    assert type(sides.left) is BinaryExpr and sides.left.op == OpType.AND \
           and type(sides.left.left) is SideExpr \
           and type(sides.left.right) is BinaryExpr and sides.left.right.op == OpType.OR \
           and type(sides.left.right.left) is SideExpr \
           and type(sides.left.right.right) is SideExpr

    assert type(sides.right) is SideExpr


def test_parse_side_group_last(prefix, suffix):
    check = "если (человек.пересекает(*л1, (справа и (сверху или снизу)))):;"

    event: EventExpr = Parser(prefix + check + suffix).parse().processing.items[0].event
    assert type(event) is EventExpr and len(event.args) == 2

    sides: BinaryExpr = event.args[pn.SIDES]
    assert type(sides) is BinaryExpr and sides.op == OpType.AND \
           and type(sides.left) is SideExpr \
           and type(sides.right) is BinaryExpr and sides.right.op == OpType.OR \
           and type(sides.right.left) is SideExpr and type(sides.right.right) is SideExpr


def test_parse_side_group_first(prefix, suffix):
    check = "если (человек.пересекает(*л1, ((сверху или снизу) и справа))):;"

    event: EventExpr = Parser(prefix + check + suffix).parse().processing.items[0].event
    assert type(event) is EventExpr and len(event.args) == 2

    sides: BinaryExpr = event.args[pn.SIDES]
    assert type(sides) is BinaryExpr and sides.op == OpType.AND \
           and type(sides.left) is BinaryExpr and sides.left.op == OpType.OR \
           and type(sides.left.left) is SideExpr and type(sides.left.right) is SideExpr \
           and type(sides.right) is SideExpr
