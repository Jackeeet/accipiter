import redpoll.resources.translation.paramnames as pn
from redpoll.types import DataType

param_types = {
    pn.AREA: {DataType.AREA},
    pn.COLOUR: {DataType.COLOUR},
    pn.COUNTER: {DataType.COUNTER},
    pn.LINE: {DataType.LINE},
    pn.MESSAGE: {DataType.STRING},
    pn.NUMBER: {DataType.INT},
    pn.PERIOD: {DataType.INT},
    # pn.SIDE: {DataType.},
    pn.SEGMENT: {DataType.SEGMENT},
    pn.TOOL: {DataType.SEGMENT, DataType.Arc, DataType.AREA, DataType.LINE, DataType.COUNTER},
}
