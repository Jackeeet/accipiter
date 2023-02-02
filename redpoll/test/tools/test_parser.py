import pytest

from redpoll.analyzer.syntactic import ParseError, Parser
from redpoll.expressions import *
from redpoll.resources import keywords as kw
from redpoll.types import DataType


@pytest.fixture
def prefix():
    return "объекты: ; инструменты: "


@pytest.fixture
def suffix():
    return " ; обработка: ;"


def test_parse_named_point(prefix, suffix):
    tool = "*точка_1: .(1, 2);"

    program: ProgramExpr = Parser(prefix + tool + suffix).parse()

    expr: PointExpr = program.tools.items[0]
    assert type(expr) is PointExpr
    assert type(expr.id) is ToolIdExpr and expr.id.value == "точка_1"

    assert len(expr.params.items()) == 1
    assert kw.POINT in expr.params and expr.params[kw.POINT].value == (1, 2)


def test_parse_segment_named_params(prefix, suffix):
    tool = "*о1: прямая, от=.(2, 2), до=.(4, 4);"

    program: ProgramExpr = Parser(prefix + tool + suffix).parse()

    expr: SegmentExpr = program.tools.items[0]
    assert type(expr) is SegmentExpr
    assert len(expr.params.items()) == 4 \
           and kw.FROM in expr.params \
           and kw.TO in expr.params

    from_expr: CoordsExpr = expr.params[kw.FROM]
    to_expr: CoordsExpr = expr.params[kw.TO]
    assert type(from_expr) is CoordsExpr and type(to_expr) is CoordsExpr
    assert from_expr.value == (2, 2) and to_expr.value == (4, 4)

    # default parameters must be set as the syntactic analysis goes
    assert kw.COLOUR in expr.params and kw.THICKNESS in expr.params
    # default colour is black
    colour: ColourExpr = expr.params[kw.COLOUR]
    assert type(colour) is ColourExpr and colour.type == DataType.COLOUR
    assert colour.value == (0, 0, 0)
    # default line thickness is 1
    assert expr.params[kw.THICKNESS].value == 1


def test_parse_colour_param(prefix, suffix):
    tool = "*о1: прямая, от=.(2, 2), до=.(4, 4), цвет=rgb(255, 128, 0);"

    program: ProgramExpr = Parser(prefix + tool + suffix).parse()

    expr: SegmentExpr = program.tools.items[0]
    assert len(expr.params) == 4
    assert kw.COLOUR in expr.params and kw.THICKNESS in expr.params
    colour: ParamsExpr = expr.params[kw.COLOUR]
    assert colour.value == (255, 128, 0)


def test_parse_identifier_param(prefix, suffix):
    tool = "*д1: дуга, центр=*точка_1, радиус=1, уголОт=0, уголДо=-180;"

    program: ProgramExpr = Parser(prefix + tool + suffix).parse()

    expr: ArcExpr = program.tools.items[0]
    assert kw.CENTER in expr.params
    assert type(expr.params[kw.CENTER]) is ToolIdExpr
    assert expr.params[kw.CENTER].value == "точка_1"


def test_parse_composite(prefix, suffix):
    area_str = "*о1_1: зона, состав=...(\n" + \
               "  *о1 ;\n" + \
               "  дуга, центр=.(3, 3), радиус=1, уголОт=0, уголДо=180\n" + \
               ");"
    program: ProgramExpr = Parser(prefix + area_str + suffix).parse()

    expr: AreaExpr = program.tools.items[0]
    assert type(expr) is AreaExpr and expr.id.value == "о1_1"

    params = expr.params
    assert len(params) == 3 and kw.COMPONENTS in params

    content: ToolPartsExpr = params[kw.COMPONENTS]
    assert type(content) is ToolPartsExpr
    assert len(content.parts) == 2 \
           and type(content.parts[0]) is ToolIdExpr \
           and content.parts[0].value == "о1"

    inner_tool: ArcExpr = content.parts[1]
    assert type(inner_tool) is ArcExpr \
           and kw.RADIUS in inner_tool.params \
           and inner_tool.params[kw.RADIUS].value == 1


def test_parse_multiple_tools_block(prefix, suffix):
    tool = """ *т_1: .(2,3);
               *line: прямая, от=*т_1, до=.(4,5);
               *а: зона, состав=...( прямая, от=*т_1, до=.(5,4); *line; *т_1 );"""

    expr: ProgramExpr = Parser(prefix + tool + suffix).parse()
    assert type(expr) is ProgramExpr

    items: list[ToolExpr] = expr.tools.items
    assert len(items) == 3
    assert type(items[0]) is PointExpr and items[0].id.value == "т_1"
    assert type(items[1]) is SegmentExpr and items[1].id.value == "line"
    assert type(items[2]) is AreaExpr and items[2].id.value == "а"


def test_parse_single_part_composite(prefix, suffix):
    tool = "*тр1: линия, состав=...(*о1);"
    program: ProgramExpr = Parser(prefix + tool + suffix).parse()

    expr: LineExpr = program.tools.items[0]
    assert type(expr) is LineExpr and expr.id.value == "тр1"
    assert len(expr.params) == 3 and kw.COMPONENTS in expr.params
    content: ToolPartsExpr = expr.params[kw.COMPONENTS]

    assert len(content.parts) == 1
    assert type(content.parts[0]) is ToolIdExpr and content.parts[0].value == "о1"


def test_raise_on_invalid_id(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "о1: прямая, от=.(2, 2), до=.(4, 4);" + suffix).parse()
    assert "[match]" in str(error.value)


def test_raise_on_empty_composite(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*о1: зона, состав=...();" + suffix).parse()
    assert "[Часть составного инструмента]" in str(error.value)


def test_raise_on_empty_parts(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*о1: зона, состав=...(;;);" + suffix).parse()
    assert "[Часть составного инструмента]" in str(error.value)


def test_raise_on_named_tool_part(prefix, suffix):
    tool = " *о1_1: зона, состав=...(\n" + \
           "  *x: дуга, центр=.(3, 3), радиус=1, уголОт=0, уголДо=180\n" + \
           ");"
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + tool + suffix).parse()


def test_raise_on_random_name_tool_part(prefix, suffix):
    tool = " *о1_1: зона, состав=...(\n" + \
           "  x: дуга, центр=.(3, 3), радиус=1, уголОт=0, уголДо=180\n" + \
           ");"
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + tool + suffix).parse()


def test_raise_on_unknown_type(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*р1: радиус, (0, 1);" + suffix).parse()
    assert "[Тип инструмента]" in str(error.value)


def test_raise_on_invalid_parameter(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*о1: прямая, дуга=2;" + suffix).parse()
    assert "[Параметр инструмента]" in str(error.value)


def test_raise_on_duplicate_tool_param(prefix, suffix):
    tool = "    *л1: прямая, от=.(20, 30), от=.(12, 12), до=.(12, 12);"
    source = prefix + tool + suffix
    with pytest.raises(ParseError) as error:
        _ = Parser(source).parse()
    assert "[Параметр инструмента]" in str(error.value)


def test_raise_on_invalid_value(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*о1: прямая, от=радиус, до=.(2,2);" + suffix).parse()
    assert "[Значение параметра]" in str(error.value)


def test_raise_on_invalid_colour(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*т1: .(0, 0), цвет=rgb(0, 0, \"синий\");" + suffix).parse()
    assert "[read_value]" in str(error.value)


def test_raise_on_unseparated_params(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*о1: прямая, от=.(2,2) до=.(2,2);" + suffix).parse()
    assert "[match]" in str(error.value)


def test_raise_on_unnamed_params(prefix, suffix):
    with pytest.raises(ParseError) as error:
        _ = Parser(prefix + "*о1: прямая, .(2, 2), .(4, 4);" + suffix).parse()
    assert "[Параметр инструмента]" in str(error.value)
