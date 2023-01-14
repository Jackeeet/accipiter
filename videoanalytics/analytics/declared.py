__all__ = ['object_kinds', 'tools', 'conditions']
print("'declared' loaded")

from .declarable.actions import *
from .declarable.condition import *
from .declarable.events import *
from .declarable.tools import *

object_kinds = ['person', 'car', ]
tools: dict[int, Tool | tuple[int, int]] = dict()

tools[0] = Segment(colour=(255, 0, 0),thickness=1,end=(50, 60),start=(50, 50),)
tools[1] = Counter(colour=(0, 0, 0),thickness=1,start=0,step=1,)

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[int, Action | Event] = dict()
conditions: list[Condition] = []

