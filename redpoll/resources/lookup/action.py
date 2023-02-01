from redpoll.resources import keywords as kw
from redpoll.resources.lookup.params import ParamName as pn

""" Обязательные параметры действий

При описании действия аргументы должны быть переданы в том же порядке, 
что и параметры в соответствующем действию множестве.
"""
required_params = {
    kw.ALERT: [pn.MESSAGE],
    kw.SAVE: [],
    kw.INCREMENT: [pn.COUNTER],
    kw.DECREMENT: [pn.COUNTER],
    kw.RESET: [pn.COUNTER],
    kw.FLASH: [pn.DRAWABLE, pn.COLOUR]
}

""" Необязательные параметры действий 

Суммарное множество параметров должно быть отсортировано 
в порядке {required, extra}.
"""

extra_params = {
    kw.ALERT: [],
    kw.SAVE: [pn.MESSAGE],
    kw.INCREMENT: [],
    kw.DECREMENT: [],
    kw.RESET: [],
    kw.FLASH: []
}

""" Общие списки параметров действий """
param_lists = {
    param_name: [*required, *extra]
    for ((param_name, required), (_, extra))
    in zip(required_params.items(), extra_params.items())
}
