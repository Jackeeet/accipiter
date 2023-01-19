from redpoll.resources import keywords as kw
from redpoll.resources.translation import paramnames as pn

""" Обязательные параметры для действия

При описании действия аргументы должны быть переданы в том же порядке, 
что и параметры в соответствующем действию множестве.
"""
required_params = {
    kw.ALERT: {pn.MESSAGE},
    kw.SAVE: set(),
    kw.INCREMENT: {pn.COUNTER},
    kw.DECREMENT: {pn.COUNTER},
    kw.RESET: {pn.COUNTER},
    kw.SET_COLOUR: {pn.TOOL, pn.COLOUR}
}

""" Необязательные параметры действий 

Суммарное множество параметров должно быть отсортировано 
в порядке {required, extra}.
"""

extra_params = {
    kw.ALERT: set(),
    kw.SAVE: {pn.MESSAGE},
    kw.INCREMENT: set(),
    kw.DECREMENT: set(),
    kw.RESET: set(),
    kw.SET_COLOUR: set()
}
