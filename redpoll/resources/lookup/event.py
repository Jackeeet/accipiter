from redpoll.resources import keywords as kw, paramnames as pn

""" Обязательные параметры событий

При описании события аргументы должны быть переданы в том же порядке, 
что и параметры в соответствующем событию множестве.
"""

required_params = {
    kw.CROSSING: [pn.TOOLS],

    kw.ENTERING: [pn.AREA],
    kw.IS_IN: [pn.AREA],
    kw.LEAVING: [pn.AREA],

    kw.DIVERTS_FROM: [pn.LINE],
    kw.SPEEDING_UP: [],
    kw.SLOWING_DOWN: [],
    kw.STILL: [],

    kw.APPEARS: [],
    kw.DISAPPEARS: [],

    kw.EQUALS: [pn.NUMBER],
    kw.ABOVE: [pn.NUMBER],
    kw.BELOW: [pn.NUMBER],
}

""" Необязательные параметры событий 

Суммарное множество параметров должно быть отсортировано 
в порядке {required, extra}.
"""

extra_params = {
    kw.CROSSING: [pn.SIDES],

    kw.ENTERING: [],  # this should take a binary chain of components
    kw.IS_IN: [pn.PERIOD],
    kw.LEAVING: [],  # this should take a binary chain of components

    kw.DIVERTS_FROM: [],
    kw.SPEEDING_UP: [],
    kw.SLOWING_DOWN: [],
    kw.STILL: [pn.PERIOD],

    kw.APPEARS: [],
    kw.DISAPPEARS: [],

    kw.EQUALS: [],
    kw.ABOVE: [],
    kw.BELOW: [],
}

""" Общие списки параметров событий """
param_lists = {
    param_name: [*required, *extra]
    for ((param_name, required), (_, extra))
    in zip(required_params.items(), extra_params.items())
}
