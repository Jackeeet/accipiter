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
