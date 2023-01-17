import pytest

from redpoll.types import DataType
from redpoll.analyzer.syntactic import ParseError, Parser
from redpoll.expressions import AreaExpr, CurveExpr, LineExpr, PointExpr, ProgramExpr, SegmentExpr, ToolExpr, ToolIdExpr
from redpoll.expressions.paramexpressions import ToolPartsExpr, AtomicExpr, ParamsExpr
from redpoll.resources import keywords as kw
from redpoll.resources.messages import parseerrors as err


@pytest.fixture
def prefix():
    return "объекты: ; инструменты: "


@pytest.fixture
def suffix():
    return " ; обработка: ;"


def test_parse_named_point(prefix, suffix):
    parser = Parser(prefix + "*точка_1: (1, 2);" + suffix)

    program: ProgramExpr = parser.parse()

    expr: PointExpr = program.tools.items[0]
    assert type(expr) is PointExpr
    assert type(expr.id) is ToolIdExpr
    assert expr.id.value == "точка_1"

    assert len(expr.params.items()) == 1

    assert kw.POINT in expr.params
    assert expr.params[kw.POINT] == AtomicExpr((1, 2), DataType.COORDS)


def test_parse_segment_named_params(prefix, suffix):
    parser = Parser(prefix + "*о1: прямая, от=(2, 2), до=(4, 4);" + suffix)

    program: ProgramExpr = parser.parse()

    expr: SegmentExpr = program.tools.items[0]
    assert type(expr) is SegmentExpr
    assert len(expr.params.items()) == 4
    assert kw.FROM in expr.params and kw.TO in expr.params
    from_expr: ParamsExpr = expr.params[kw.FROM]
    to_expr: ParamsExpr = expr.params[kw.TO]
    assert type(from_expr) is AtomicExpr and type(to_expr) is AtomicExpr
    assert from_expr.value == (2, 2)
    assert to_expr.value == (4, 4)

    # default parameters must be set as the syntactic analysis goes
    assert kw.COLOUR in expr.params and kw.THICKNESS in expr.params
    # default colour is black
    colour: ParamsExpr = expr.params[kw.COLOUR]
    assert type(colour) is AtomicExpr and colour.type == DataType.COLOUR
    assert colour.value == (0, 0, 0)
    # default line thickness is 1
    assert expr.params[kw.THICKNESS] == AtomicExpr(1, DataType.INT)


def test_parse_colour_param(prefix, suffix):
    parser = Parser(prefix + "*о1: прямая, от=(2, 2), до=(4, 4), цвет=rgb(255, 128, 0);" + suffix)

    program: ProgramExpr = parser.parse()

    expr: SegmentExpr = program.tools.items[0]
    assert len(expr.params) == 4
    assert kw.COLOUR in expr.params and kw.THICKNESS in expr.params
    colour: ParamsExpr = expr.params[kw.COLOUR]
    assert colour.value == (255, 128, 0)


def test_parse_identifier_param(prefix, suffix):
    parser = Parser(prefix + "*д1: дуга, центр=*точка_1, радиус=1, уголОт=0, уголДо=-180;" + suffix)

    program: ProgramExpr = parser.parse()

    expr: CurveExpr = program.tools.items[0]
    assert kw.CENTER in expr.params
    assert type(expr.params[kw.CENTER]) is ToolIdExpr
    assert expr.params[kw.CENTER].value == "точка_1"


def test_parse_composite(prefix, suffix):
    area_str = "*о1_1: зона, состав=...(\n" + \
               "  *о1 ;\n" + \
               "  дуга, центр=(3, 3), радиус=1, уголОт=0, уголДо=180\n" + \
               ");"
    parser = Parser(prefix + area_str + suffix)

    program: ProgramExpr = parser.parse()

    expr: AreaExpr = program.tools.items[0]
    assert type(expr) is AreaExpr
    assert expr.id.value == "о1_1"

    params = expr.params
    assert len(params) == 3
    assert kw.CONTENTS in params
    content: ToolPartsExpr = params[kw.CONTENTS]
    assert type(content) is ToolPartsExpr
    assert len(content.parts) == 2
    assert type(content.parts[0]) is ToolIdExpr
    assert content.parts[0].value == "о1"
    assert type(content.parts[1]) is CurveExpr
    inner_tool: CurveExpr = content.parts[1]
    assert kw.RADIUS in inner_tool.params
    assert inner_tool.params[kw.RADIUS] == AtomicExpr(1, DataType.INT)


def test_parse_multiple_tools_block(prefix, suffix):
    parser = Parser(prefix +
                    "   *т_1: (2,3);\n" +
                    "   *line: прямая, от=*т_1, до=(4,5);\n" +
                    "   *а: зона, состав=...(\n"
                    "      прямая, от=*т_1, до=(5,4);\n"
                    "      *line;\n"
                    "      *т_1\n"
                    "   );\n" + suffix)

    expr: ProgramExpr = parser.parse()

    assert type(expr) is ProgramExpr

    items: list[ToolExpr] = expr.tools.items
    assert len(items) == 3

    assert type(items[0]) is PointExpr
    assert items[0].id.value == "т_1"

    assert type(items[1]) is SegmentExpr
    assert items[1].id.value == "line"

    assert type(items[2]) is AreaExpr
    assert items[2].id.value == "а"


def test_parse_single_part_composite(prefix, suffix):
    parser = Parser(prefix + "*тр1: линия, состав=...(*о1);" + suffix)

    program: ProgramExpr = parser.parse()

    expr: LineExpr = program.tools.items[0]
    assert type(expr) is LineExpr
    assert expr.id.value == "тр1"

    assert len(expr.params) == 3
    assert kw.CONTENTS in expr.params
    content: ToolPartsExpr = expr.params[kw.CONTENTS]
    assert len(content.parts) == 1
    assert type(content.parts[0]) is ToolIdExpr
    assert content.parts[0].value == "о1"


def test_raise_on_invalid_id(prefix, suffix):
    parser = Parser(prefix + "о1: прямая, от=(2, 2), до=(4, 4);" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[match]" in str(error.value)


def test_raise_on_empty_composite(prefix, suffix):
    parser = Parser(prefix + "*о1: зона, состав=...();" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Часть составного инструмента]" in str(error.value)


def test_raise_on_empty_parts(prefix, suffix):
    parser = Parser(prefix + "*о1: зона, состав=...(;;);" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Часть составного инструмента]" in str(error.value)


def test_raise_on_named_tool_part(prefix, suffix):
    tool = " *о1_1: зона, состав=...(\n" + \
           "  *x: дуга, центр=(3, 3), радиус=1, уголОт=0, уголДо=180\n" + \
           ");"
    parser = Parser(prefix + tool + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()


def test_raise_on_random_name_tool_part(prefix, suffix):
    tool = " *о1_1: зона, состав=...(\n" + \
           "  x: дуга, центр=(3, 3), радиус=1, уголОт=0, уголДо=180\n" + \
           ");"
    parser = Parser(prefix + tool + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()


def test_raise_on_unknown_type(prefix, suffix):
    parser = Parser(prefix + "*р1: радиус, (0, 1);" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Тип инструмента]" in str(error.value)


def test_raise_on_invalid_parameter(prefix, suffix):
    parser = Parser(prefix + "*о1: прямая, дуга=2;" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Параметр инструмента]" in str(error.value)


def test_raise_on_duplicate_tool_param(prefix, suffix):
    source = prefix + \
             "    *л1: прямая, от=(20, 30), от=(12, 12), до=(12, 12);" + \
             suffix
    parser = Parser(source)

    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Параметр инструмента]" in str(error.value)


def test_raise_on_invalid_value(prefix, suffix):
    parser = Parser(prefix + "*о1: прямая, от=радиус, до=(2,2);" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Значение параметра]" in str(error.value)


def test_raise_on_non_tool_id_tool_param_value(prefix, suffix):
    parser = Parser(prefix + "*л1: прямая, от=(20, 30), до=человек;" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Значение параметра]" in str(error.value)


def test_raise_on_invalid_colour(prefix, suffix):
    parser = Parser(prefix + "*т1: (0, 0), цвет=rgb(0, 0, \"синий\");" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[read_value]" in str(error.value)


def test_raise_on_unseparated_params(prefix, suffix):
    parser = Parser(prefix + "*о1: прямая, от=(2,2) до=(2,2);" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[match]" in str(error.value)


def test_raise_on_unnamed_params(prefix, suffix):
    parser = Parser(prefix + "*о1: прямая, (2, 2), (4, 4);" + suffix)
    with pytest.raises(ParseError) as error:
        _ = parser.parse()
    assert "[Параметр инструмента]" in str(error.value)
