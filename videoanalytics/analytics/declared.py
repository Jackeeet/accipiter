__all__ = ['object_kinds', 'tools', 'conditions']

from videoanalytics.analytics.declarable.actions import *
from videoanalytics.analytics.declarable.condition import *
from videoanalytics.analytics.declarable.events import *
from videoanalytics.analytics.declarable.tools import *
from videoanalytics.models import Coords

print("'declared' loaded")
object_kinds = ['person', ]
tools: dict[int, Tool | tuple[int, int]] = dict()

tools[0] = Segment(colour=(255, 0, 0),thickness=2,start=Coords(320, 0),end=Coords(320, 360),)
tools[1] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

conditions.append(Condition(
    Event(crosses,object_kinds[0],{'segment': tools[0],}),
    [Action(increment,{'counter': tools[1],}),Action(flash,{'drawable': object_kinds[0],'colour': (0, 255, 0),}),]
))
