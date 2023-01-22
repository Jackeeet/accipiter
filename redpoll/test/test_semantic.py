import pytest

from redpoll.analyzer.semantic import Analyzer, SemanticError
from redpoll.resources.messages import semanticerrors as err


def test_unique_object_ids():
    source = "объекты: человек; автомобиль; ; инструменты:; обработка:;"
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_duplicate_object_ids():
    source = "объекты: человек; человек; ; инструменты:; обработка:;"
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.duplicated_object_id() in str(error.value)


def test_unique_tool_ids():
    source = """объекты:; инструменты:
        *о1: прямая, от=(2, 2), до=(4, 4);
        *д1: дуга, центр=(2, 2), радиус=1, уголОт=0, уголДо=-180;
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_duplicate_tool_ids():
    source = """объекты:; инструменты:
        *д1: прямая, от=(2, 2), до=(4, 4);
        *д1: дуга, центр=(3, 3), радиус=1, уголОт=0, уголДо=-180;
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.duplicated_tool_id() in str(error.value)


def test_unique_processing_ids():
    source = """объекты:; инструменты:; обработка:
        _действие1: сохранить();
        _действие2: сохранить();
    ;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_duplicate_processing_ids():
    source = """объекты:; инструменты:; обработка:
        _действие1: сохранить();
        _действие1: сохранить();
    ;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.duplicated_processing_id() in str(error.value)


# ---- tool params ----

def test_id_as_tool_param():
    source = """объекты:; инструменты:
        *т1: (40, 50);
        *л1: прямая, от=(20, 30), до=*т1;
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_self_id_as_tool_param():
    source = """объекты:; инструменты:
        *л1: прямая, от=(20, 30), до=*л1;
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.self_id_as_param_value() in str(error.value)


def test_raise_on_undefined_id_as_tool_param():
    source = """объекты:; инструменты:
        *л1: прямая, от=(20, 30), до=*т1;
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.undeclared_tool_variable("т1") in str(error.value)


# todo test all tool types
def test_raise_on_unexpected_tool_params():
    source = """объекты:; инструменты:
        *л1: прямая, радиус=2, от=(20, 30), до=(12, 12);
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unexpected_parameter_name("радиус") in str(error.value)


# todo test all tool types
def test_only_required_tool_params():
    source = """объекты:; инструменты:
        *л1: прямая, от=(20, 30), до=(40, 50);
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_missing_required_tool_param():
    source = """объекты:; инструменты:
        *л1: прямая, от=(20, 30);
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.missing_required_tool_param() in str(error.value)


# todo test all param kinds
def test_tool_param_value_matching_param_type():
    source = """объекты:; инструменты:
        *л2: прямая, до=(50, 60), от=(50, 50), цвет=rgb(255, 0, 0), толщина=1;
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_tool_param_type_mismatch():
    source = """объекты:; инструменты:
        *л2: прямая, до = rgb(255, 0, 0), от = (50, 50), цвет = rgb(255, 0, 0), толщина = 1;
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.parameter_type_mismatch() in str(error.value)


# ---- tool parts ----

def test_id_as_tool_part():
    source = """объекты:; инструменты:
        *л1: прямая, от = (20, 20), до = (20, 40);
        *з1: зона, состав = ...(
            *л1;
            дуга, центр = (20, 30), радиус = 10, уголОт = 90, уголДо = 270
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_raise_on_undefined_id_as_tool_part():
    source = """объекты:; инструменты:
        *л1: прямая, от = (20, 20), до = (20, 20);
        *з1: зона, состав = ...(
            *s1;
            дуга, центр = (20, 30), радиус = 20, уголОт = 0, уголДо = 180
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.undeclared_tool_part() in str(error.value)


def test_raise_on_point_as_tool_part():
    source = """объекты:; инструменты:
        *т1: (40, 50);
        *з1: зона, состав=...(*т1);
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unsupported_tool_part_type() in str(error.value)


def test_raise_on_area_as_tool_part():
    source = """объекты:; инструменты:
        *з1: зона, состав = ...(
            прямая, от = (20, 20), до = (20, 30);
            прямая, от = (20, 30), до = (30, 30);
            прямая, от = (30, 30), до = (20, 20)
        );
        *з2: зона, состав = ...(*з1);
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unsupported_tool_part_type() in str(error.value)


# it could be useful to allow composite lines to be tool parts,
# but then I'll need to track the start and the end of the line
def test_raise_on_line_as_tool_part():
    source = """объекты:; инструменты:
        *л1: линия, состав = ...(
            прямая, от = (20, 20), до = (20, 40);
            прямая, от = (40, 40), до = (20, 40)
        );
        *з2: зона, состав = ...(*л1);
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unsupported_tool_part_type() in str(error.value)


def test_raise_on_counter_as_tool_part():
    source = """объекты:; инструменты:
        *л1: линия, состав = ...(
            прямая, от = (20, 20), до = (20, 40);
            счетчик, старт=0, шаг=1
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unsupported_tool_part_type() in str(error.value)


def test_raise_on_unconnected_area_with_segments():
    source = """объекты:; инструменты:
        *з1: зона, состав = ...(
            прямая, от = (20, 20), до = (20, 30);
            прямая, от = (20, 30), до = (30, 30);
            прямая, от = (30, 30), до = (30, 20);
            прямая, от = (30, 20), до = (20, 25)
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unconnected_area() in str(error.value)


def test_raise_on_unconnected_area_with_arc():
    source = """объекты:; инструменты:
        *з1: зона, состав = ...(
            прямая, от = (20, 20), до = (20, 30);
            дуга, центр = (20, 30), радиус = 20, уголОт = 0, уголДо = 180
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unconnected_area in str(error.value)


def test_raise_on_unconnected_line():
    source = """объекты:; инструменты:
        *л1: линия, состав = ...(
            прямая, от = (20, 20), до = (20, 30);
            прямая, от = (40, 40), до = (30, 40)
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.unconnected_line() in str(error.value)


def test_raise_on_duplicated_segment():
    source = """объекты:; инструменты:
        *з1: зона, состав = ...(
            прямая, от = (30, 20), до = (40, 40);
            прямая, от = (40, 40), до = (20, 40);
            прямая, от = (20, 40), до = (30, 20);
            прямая, от = (20, 40), до = (30, 20)
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.duplicated_tool_part() in str(error.value)


def test_raise_on_duplicated_arc():
    source = """объекты:; инструменты:
        *f1: линия, состав = ...(
            дуга, центр = (20, 30), радиус = 20, уголОт = 0, уголДо = 180;
            дуга, центр = (20, 30), радиус = 20, уголОт = 0, уголДо = 180
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    with pytest.raises(SemanticError) as error:
        _ = analyzer.analyze()
    assert err.duplicated_tool_part() in str(error.value)


def test_two_arcs_making_circle():
    source = """объекты:; инструменты:
        *з1: зона, состав = ...(
            дуга, центр = (20, 30), радиус = 20, уголОт = 0, уголДо = 90;
            дуга, центр = (20, 30), радиус = 20, уголОт = 90, уголДо = 360
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success


def test_arc_and_line_making_area():
    source = """объекты:; инструменты:
        *л1: прямая, от = (20, 20), до = (20, 40);
        *з1: зона, состав = ...(
            *л1;
            дуга, центр = (20, 30), радиус = 10, уголОт = 90, уголДо = 270
        );
    ; обработка:;"""
    analyzer = Analyzer(source)

    success = analyzer.analyze()
    assert success
