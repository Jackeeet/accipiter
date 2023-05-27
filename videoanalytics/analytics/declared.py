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

tools[0] = Scene(colour=(0, 0, 0), thickness=0)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

conditions.append(Condition(
    Event(appears,object_kinds[0],{}),
    [Action(alert,{'message': 'чел',}),]
))
