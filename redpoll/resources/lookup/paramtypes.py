import redpoll.resources.paramnames as pn
from redpoll.types import DataType

param_types = {
    pn.AREA: {DataType.AREA},
    pn.COLOUR: {DataType.COLOUR},
    pn.COUNTER: {DataType.COUNTER},
    pn.DRAWABLE: {DataType.OBJECT_ID},
    pn.LINE: {DataType.LINE},
    pn.MESSAGE: {DataType.STRING},
    pn.NUMBER: {DataType.INT},
    pn.PERIOD: {DataType.INT},
    pn.SIDES: {DataType.SIDE},
    pn.SEGMENT: {DataType.SEGMENT},
    pn.TOOLS: {DataType.SEGMENT, DataType.ARC, DataType.AREA, DataType.LINE, DataType.COUNTER},
}
