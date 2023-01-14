from redpoll.analyzer.lexical.transliterator import Symbol, Transliterator

input_str = "(2, 2)"


def test_read_first():
    tlr = Transliterator(input_str)

    tlr.read_next()

    assert tlr.line == 1
    assert tlr.position == 1
    assert tlr.char == '('
    assert tlr.symbol == Symbol.LEFT_BRACKET


def test_read_to_last():
    tlr = Transliterator(input_str)

    for i in range(len(input_str)):
        tlr.read_next()

    assert tlr.line == 1
    assert tlr.position == 6
    assert tlr.char == ')'
    assert tlr.symbol == Symbol.RIGHT_BRACKET


def test_read_all():
    tlr = Transliterator(input_str)

    for i in range(len(input_str) + 1):
        tlr.read_next()

    assert tlr.line == 1
    assert tlr.position == 7
    assert tlr.symbol == Symbol.EOT


def test_read_multiline():
    tlr = Transliterator("123\n5678\nABC")

    for i in range(11):
        tlr.read_next()

    assert tlr.line == 3
    assert tlr.position == 2
    assert tlr.char == 'B'
    assert tlr.symbol == Symbol.LATIN_LETTER


def test_case_insensitive():
    tlr = Transliterator("yYзЗ")

    tlr.read_next()
    assert tlr.symbol == Symbol.LATIN_LETTER
    tlr.read_next()
    assert tlr.symbol == Symbol.LATIN_LETTER
    tlr.read_next()
    assert tlr.symbol == Symbol.LETTER
    tlr.read_next()
    assert tlr.symbol == Symbol.LETTER


def test_empty():
    tlr = Transliterator("")
    tlr.read_next()
    assert tlr.symbol == Symbol.EOT
