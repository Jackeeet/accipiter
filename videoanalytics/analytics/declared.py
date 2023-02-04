__all__ = ['object_kinds', 'tools', 'conditions']

from videoanalytics.analytics.actions import *
from videoanalytics.analytics.condition import *
from videoanalytics.analytics.events import *
from videoanalytics.analytics.tools import *
from videoanalytics.models.operators import *
from videoanalytics.models import Coords, EvalTree, Side, SideValue

print("'declared' loaded")
object_kinds = ['птица', ]
tools: dict[int, Tool | tuple[int, int]] = dict()

tools[0] = Coords(100, 100)
tools[1] = Coords(200, 100)
tools[2] = Coords(200, 200)
tools[3] = Coords(100, 200)
tools[4] = Segment(colour=(0, 0, 0),thickness=1,start=tools[0],end=tools[1],)
tools[5] = Segment(colour=(0, 0, 0),thickness=1,start=tools[1],end=tools[2],)
tools[6] = Segment(colour=(0, 0, 0),thickness=1,start=tools[2],end=tools[3],)
tools[7] = Segment(colour=(0, 0, 0),thickness=1,start=tools[3],end=tools[0],)
tools[8] = Area(colour=(0, 0, 255),thickness=2,components=[
    tools[4],
    tools[5],
    tools[6],
    tools[7],
],)
tools[9] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)
tools[10] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)
tools[11] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

conditions.append(Condition(
    Event(enters,object_kinds[0],{'area': tools[8],'tools': EvalTree(
        left=EvalTree(
        left=EvalTree(
        left=tools[4],
        op_or_val=op_or,
        right=tools[5]
    ),
        op_or_val=op_or,
        right=tools[6]
    ),
        op_or_val=op_or,
        right=tools[7]
    ),}),
    [Action(increment,{'counter': tools[9],}),Action(flash,{'drawable': object_kinds[0],'colour': (0, 255, 0),}),]
))
conditions.append(Condition(
    Event(is_inside,object_kinds[0],{'area': tools[8],'period': 10,}),
    [Action(increment,{'counter': tools[10],}),Action(flash,{'drawable': 'человек','colour': (255, 255, 255),}),]
))
conditions.append(Condition(
    Event(leaves,object_kinds[0],{'area': tools[8],'tools': EvalTree(
        left=EvalTree(
        left=EvalTree(
        left=tools[4],
        op_or_val=op_or,
        right=tools[5]
    ),
        op_or_val=op_or,
        right=tools[6]
    ),
        op_or_val=op_or,
        right=tools[7]
    ),}),
    [Action(increment,{'counter': tools[11],}),Action(flash,{'drawable': object_kinds[0],'colour': (255, 0, 0),}),]
))
