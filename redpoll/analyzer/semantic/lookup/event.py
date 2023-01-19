from redpoll.resources import keywords as kw
from redpoll.resources.translation import paramnames as pn

""" Обязательные параметры для события

При описании события аргументы должны быть переданы в том же порядке, 
что и параметры в соответствующем событию множестве.
"""

required_params = {
    kw.CROSSING: {pn.SEGMENT},
    kw.ENTERING: {pn.AREA},
    kw.LEAVING: {pn.AREA},
    kw.DIVERTS_FROM: {pn.LINE},
    kw.SPEEDING_UP: set(),
    kw.SLOWING_DOWN: set(),
    kw.STILL: set(),
    kw.APPEARS: set(),
    kw.DISAPPEARS: set(),
    kw.EQUALS: {pn.NUMBER},
    kw.ABOVE: {pn.NUMBER},
    # todo maybe add BELOW as well
}

""" Необязательные параметры событий 

Суммарное множество параметров должно быть отсортировано 
в порядке {required, extra}.
"""

extra_params = {
    kw.CROSSING: {pn.SIDE},
    kw.ENTERING: set(),
    kw.LEAVING: set(),
    kw.DIVERTS_FROM: set(),
    kw.SPEEDING_UP: set(),
    kw.SLOWING_DOWN: set(),
    kw.STILL: {pn.PERIOD},
    kw.APPEARS: set(),
    kw.DISAPPEARS: set(),
    kw.EQUALS: set(),
    kw.ABOVE: set(),
}
