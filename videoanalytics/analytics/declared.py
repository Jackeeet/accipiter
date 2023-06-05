__all__ = ['object_kinds', 'tools', 'conditions']

from videoanalytics.analytics.actions import *
from videoanalytics.analytics.condition import *
from videoanalytics.analytics.events import *
from videoanalytics.analytics.tools import *
from videoanalytics.models.operators import *
from videoanalytics.models import Coords, EvalTree, Side, SideValue

print("'declared' loaded")
object_kinds = ['автомобиль', ]
tools: dict[int, Tool | tuple[int, int]] = dict()

tools[0] = Segment(colour=(255, 122, 122),thickness=1,start=Coords(0, 363),end=Coords(848, 363),)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

conditions.append(Condition(
    Event(crosses,object_kinds[0],{'tool': tools[0],'sides': Side(SideValue('top')),}),
    [Action(flash,{'drawable': object_kinds[0],'colour': (0, 255, 0),}),]
))
conditions.append(Condition(
    Event(crosses,object_kinds[0],{'tool': tools[0],'sides': Side(SideValue('bottom')),}),
    [Action(flash,{'drawable': object_kinds[0],'colour': (0, 0, 255),}),]
))
