from redpoll.resources import keywords as kw
from redpoll.resources.translation import paramnames as pn

""" Обязательные параметры для события

При описании события аргументы должны быть переданы в том же порядке, 
что и параметры в соответствующем событию множестве.
"""

required_params = {
    kw.CROSSING: [pn.SEGMENT],
    kw.ENTERING: [pn.AREA],
    kw.LEAVING: [pn.AREA],
    kw.DIVERTS_FROM: [pn.LINE],
    kw.SPEEDING_UP: [],
    kw.SLOWING_DOWN: [],
    kw.STILL: [],
    kw.APPEARS: [],
    kw.DISAPPEARS: [],
    kw.EQUALS: [pn.NUMBER],
    kw.ABOVE: [pn.NUMBER],
    # todo maybe add BELOW as well
}

""" Необязательные параметры событий 

Суммарное множество параметров должно быть отсортировано 
в порядке {required, extra}.
"""

extra_params = {
    kw.CROSSING: [pn.SIDE],
    kw.ENTERING: [],
    kw.LEAVING: [],
    kw.DIVERTS_FROM: [],
    kw.SPEEDING_UP: [],
    kw.SLOWING_DOWN: [],
    kw.STILL: [pn.PERIOD],
    kw.APPEARS: [],
    kw.DISAPPEARS: [],
    kw.EQUALS: [],
    kw.ABOVE: [],
}
