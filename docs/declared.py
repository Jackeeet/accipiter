__all__ = ['object_kinds', 'tools', 'conditions']

from declarable.actions import *
from declarable.condition import *
from declarable.events import *
from declarable.tools import *

object_kinds = ['person', 'car', ]
tools: dict[int, Tool | tuple[int, int]] = dict()

tools[0] = (40, 50)
tools[1] = Segment(colour=(0, 0, 0),thickness=1,start=(20, 30),end=tools[0],)
tools[2] = Segment(colour=(255, 0, 0),thickness=1,end=(50, 60),start=(50, 50),)
tools[3] = Area(colour=(0, 0, 0),thickness=1,contents=[
    tools[1],
    tools[2],
    Curve(colour=(0, 0, 0),thickness=1,center=(3, 3),radius=1,start=0,end=180,),
],)
tools[4] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

declarations[0] = Action(alert,{'message': 'сообщение 1',})
declarations[1] = Action(alert,{'message': 'сообщение_3',})
conditions.append(Condition(
    Event(intersects,{'element': tools[1],}),
    [declarations[0],Action(alert,{'message': 'еще одно сообщение',}),]
))
declarations[2] = Event(intersects,{'element': tools[1],})
declarations[3] = Event(intersects,{'element': tools[2],})
declarations[4] = Action(increment,{'counter': tools[4],})
conditions.append(Condition(
    BinaryEventChain(
        left=declarations[2],
        val=op_or,
        right=declarations[3]
    ),
    [declarations[4],]
))
conditions.append(Condition(
    BinaryEventChain(
        left=Event(intersects,{'element': tools[2],}),
        val=op_and,
        right=declarations[3]
    ),
    [declarations[1],]
))
declarations[5] = Event(equals,{'count': 1000,})
conditions.append(Condition(
    declarations[5],
    [Action(alert,{'message': '1000 пересечений линии',}),Action(save,{'message': '1000 пересечений линии',}),Action(reset,{'counter': tools[4],}),]
))
