__all__ = ['object_kinds', 'tools', 'conditions']

from .declarable.actions import *
from .declarable.condition import Condition
from .declarable.events import *
from .declarable.tools import *

object_kinds = ['person', 'car', ]

tools: dict[str, Tool] = dict()

tools["line"] = Segment(start=Coords(300, 0), end=Coords(300, 400), colour=(0, 0, 255),)
tools["привет"] = (500, 300)
tools['счетчик'] = Counter(origin=(530, 290),)

tools['test'] = Area(colour=(0, 255, 255), contents=[
    Segment(start=(200, 200), end=(300, 200)),
    Segment(start=(300, 200), end=(300, 300)),
    Segment(start=(300, 300), end=(200, 300)),
    Segment(start=(200, 300), end=(200, 200)),
])

tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

declarations: dict[str, Action | Event] = dict()
conditions: list[Condition] = []

declarations["crossing"] = Event(intersects, 'person', {'seg': tools["line"]})

declarations['increment'] = Action(increment, {'counter': tools['счетчик']})
declarations['recolour'] = Action(set_colour, {'colour': (0, 255, 0)})

conditions.append(Condition(
    BinaryEventChain(None, declarations['crossing'], None),
    [declarations['increment'], declarations['recolour']]
))
# __all__ = ['object_kinds', 'tools', 'conditions']

# from declarable.actions import *
# from declarable.condition import *
# from declarable.events import *
# from declarable.tools import *

# object_kinds = ['person', 'car', ]
# tools: dict[int, Tool] = dict()

# tools[0] = (40, 50)
# tools[1] = Segment(start=(20, 30),end=tools[0],colour=(0, 0, 0),thickness=1,)
# tools[2] = Segment(end=(50, 60),start=(50, 50),colour=(255, 0, 0),thickness=1,)
# tools[3] = Area(contents=[
#     tools[1],
#     tools[2],
#     Curve(center=(3, 3),radius=1,start=0,end=180,colour=(0, 0, 0),thickness=1,),
# ],colour=(0, 0, 0),thickness=1,)
# tools[4] = Counter(start=0,step=1,colour=(0, 0, 0),thickness=1,)

# tools = {k:v for k,v in tools.items() if not isinstance(v, tuple)}

# events: dict[int, Event] = dict()
# actions: dict[int, Action] = dict()
# conditions: list[Condition] = []

