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

tools[0] = Area(colour=(255, 0, 0),thickness=2,components=[
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(323, 164),end=Coords(363, 164),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(0, 333),end=Coords(323, 164),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(0, 333),end=Coords(0, 464),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(0, 464),end=Coords(162, 464),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(162, 464),end=Coords(363, 164),),
],)
tools[1] = Area(colour=(255, 0, 0),thickness=2,components=[
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(393, 164),end=Coords(423, 164),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(423, 164),end=Coords(636, 464),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(636, 464),end=Coords(282, 464),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(282, 464),end=Coords(393, 164),),
],)
tools[2] = Area(colour=(255, 0, 0),thickness=2,components=[
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(443, 164),end=Coords(473, 164),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(473, 164),end=Coords(848, 333),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(848, 333),end=Coords(848, 464),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(848, 464),end=Coords(748, 464),),
    Segment(colour=(0, 0, 0),thickness=1,start=Coords(748, 464),end=Coords(443, 164),),
],)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

conditions.append(Condition(
    EvalTree(
        left=EvalTree(
        left=Event(enters,object_kinds[0],{'area': tools[0],'tools': None,}),
        op_or_val="op_or",
        right=Event(enters,object_kinds[0],{'area': tools[2],'tools': None,})
    ),
        op_or_val="op_or",
        right=Event(enters,object_kinds[0],{'area': tools[1],'tools': None,})
    ),
    [Action(flash,{'drawable': object_kinds[0],'colour': (255, 255, 255),}),]
))
