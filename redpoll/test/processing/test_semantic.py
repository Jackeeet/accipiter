import pytest

from redpoll.analyzer.semantic import Analyzer, SemanticError
from redpoll.analyzer.token import Token, TokenKind
import redpoll.expressions
from redpoll.resources.lookup import event
from redpoll.resources.messages import semanticerrors as err
from redpoll.types import OpType


def test_unique_ids():
    source = """объекты:; инструменты:; обработка:
        _действие1: сохранить();
        _действие2: сохранить();
    ;"""
    Analyzer(source).analyze()
    # failure WILL raise an exception, so assert runs only if no errors are found
    assert True


def test_raise_on_duplicate_ids():
    source = """объекты:; инструменты:; обработка:
        _действие1: сохранить();
        _действие1: сохранить();
    ;"""
    with pytest.raises(SemanticError) as error:
        _ = Analyzer(source).analyze()
    assert err.duplicated_processing_id() in str(error.value)


# ---- events ----

@pytest.fixture
def event_source_prefix():
    return """ объекты: человек;; 
    инструменты: 
        *а: прямая, от=!(10, 10), до=!(20, 20);
        *b: прямая, от=!(20, 20), до=!(20, 10);
        *в: прямая, от=!(20, 10), до=!(10, 10);
        *д: дуга, центр=!(30, 30), радиус=10, уголОт=90, уголДо=180;
        *з: зона, состав=...(*а; *b; *в);
        *сч: счетчик, старт=0, шаг=1;
    ; обработка: """


valid_event_sources = [
    """ _п1: человек.пересекает(*а);;""",
    """ _в1: человек.входитВ(*з);; """,
    """ _н1: человек.находитсяВ(*з);;""",
    """ _в1: человек.покидает(*з);; """,

    """ _п1: человек.пересекает(*а, слева или справа);
        _п2: человек.пересекает(*а, сверху или снизу и справа);
        _п3: человек.пересекает(*а, (сверху или снизу) и справа;;""",
    """ _в1: человек.входитВ(*з, *а или *b);
        _в2: человек.входитВ(*з, *в);
        _в3: человек.входитВ(*з, *а и *в);; """,
    """ _н1: человек.находитсяВ(*з, 20);;""",
    """ _в1: человек.покидает(*з, *а или *b);
        _в2: человек.покидает(*з, *в);
        _в3: человек.покидает(*з, *а и *в);; """,

    """ _сч: *сч.превышает(200);; """,
    """ _сч: *сч.равен(200);; """,
    """ _сч: *сч.ниже(200);; """,
]

left_token = Token(TokenKind.SIDE, "слева", -1, -1)
right_token = Token(TokenKind.SIDE, "справа", -1, -1)
top_token = Token(TokenKind.SIDE, "сверху", -1, -1)
bottom_token = Token(TokenKind.SIDE, "снизу", -1, -1)
zone_components = redpoll.expressions.BinaryExpr(
    redpoll.expressions.BinaryExpr(redpoll.expressions.ToolIdExpr("а"), OpType.OR, redpoll.expressions.ToolIdExpr("b")),
    OpType.OR,
    redpoll.expressions.ToolIdExpr("в")
)

default_values = [
    redpoll.expressions.BinaryExpr(
        redpoll.expressions.BinaryExpr(redpoll.expressions.SideExpr(left_token), OpType.OR,
                                       redpoll.expressions.SideExpr(right_token)),
        OpType.OR,
        redpoll.expressions.BinaryExpr(redpoll.expressions.SideExpr(top_token), OpType.OR,
                                       redpoll.expressions.SideExpr(bottom_token))
    ),
    zone_components,
    zone_components,
    zone_components,
]

invalid_event_sources = [
    ("""_п: человек.пересекает();;""", err.missing_required_event_arg()),
    ("""_в: человек.входитВ();; """, err.missing_required_event_arg()),
    ("""_в: человек.находитсяВ();; """, err.missing_required_event_arg()),
    ("""_в: человек.покидает();; """, err.missing_required_event_arg()),
    ("""_сч: *сч.равен();; """, err.missing_required_event_arg()),
    ("""_сч: *сч.превышает();; """, err.missing_required_event_arg()),
    ("""_сч: *сч.ниже();; """, err.missing_required_event_arg()),

    ("""_п: человек.пересекает("линия");;""", err.arg_type_mismatch()),
    ("""_в: человек.входитВ(20);; """, err.arg_type_mismatch()),
    ("""_в: человек.находитсяВ(20, *з);; """, err.arg_type_mismatch()),
    ("""_в: человек.покидает(20);; """, err.arg_type_mismatch()),
    ("""_сч: *сч.равен("20");; """, err.arg_type_mismatch()),
    ("""_сч: *сч.превышает("20");; """, err.arg_type_mismatch()),
    ("""_сч: *сч.ниже("20");; """, err.arg_type_mismatch()),
]


@pytest.mark.parametrize("source", valid_event_sources)
def test_valid_event_args(source, event_source_prefix):
    Analyzer(event_source_prefix + source).analyze()
    assert True


@pytest.mark.parametrize("source, values", zip(valid_event_sources[:4], default_values))
def test_fills_optional_args_with_default_values(source, values, event_source_prefix):
    ast: redpoll.expressions.ProgramExpr = Analyzer(event_source_prefix + source).analyze()
    expr: redpoll.expressions.EventExpr = ast.processing.items[0]
    assert len(expr.args) == len(event.param_lists[expr.name.value])

    extra_values = expr.args.values()[len(event.required_params):]
    for (arg, expected) in zip(extra_values, values):
        assert arg == expected


@pytest.mark.parametrize("source, err_msg", invalid_event_sources)
def test_raise_on_invalid_event_args(source, err_msg, event_source_prefix):
    with pytest.raises(SemanticError) as error:
        _ = Analyzer(event_source_prefix + source).analyze()
    assert err_msg in str(error.value)

# ---- actions ----
