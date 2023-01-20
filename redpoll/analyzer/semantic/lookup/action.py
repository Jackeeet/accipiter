from redpoll.resources import keywords as kw
from redpoll.resources.translation import paramnames as pn

""" Обязательные параметры для действия

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
