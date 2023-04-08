__all__ = ['object_kinds', 'tools', 'conditions']

from videoanalytics.analytics.actions import *
from videoanalytics.analytics.condition import *
from videoanalytics.analytics.events import *
from videoanalytics.analytics.tools import *
from videoanalytics.models.operators import *
from videoanalytics.models import Coords, EvalTree, Side, SideValue

print("'declared' loaded")
object_kinds = ['человек', ]
tools: dict[int, Tool | tuple[int, int]] = dict()

# tools[0] = Segment(colour=(255, 0, 0),thickness=2,start=Coords(320, 0),end=Coords(320, 360),)
tools[0] = Segment(colour=(255, 0, 0),thickness=2,start=Coords(0, 100),end=Coords(640, 100),)
tools[1] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

conditions.append(Condition(
    Event(crosses,object_kinds[0],{'tool': tools[0],'sides': None,}),
    [Action(increment,{'counter': tools[1],}),Action(flash,{'drawable': object_kinds[0],'colour': (0, 255, 0),}),]
))
