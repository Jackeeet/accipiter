__all__ = ['object_kinds', 'tools', 'conditions']

from declarable.actions import *
from declarable.condition import Condition
from declarable.events import *
from declarable.tools import *


object_kinds = ['person', 'car']
tools: dict[str, Tool] = dict()
events: dict[str, Event] = dict()
actions: dict[str, Action] = dict()
conditions: list[Condition] = []


tools["askslkf"] = Segment(Coords(300, 0), Coords(300, 400), colour=(0, 0, 255))
tools["привет"] = Point((500, 300), (0, 0, 255))
tools['счетчик'] = Counter(origin=(530, 290))

events["dkljfa"] = Event(intersects, 'person', {'seg': tools["askslkf"]})

actions['dkdkkd'] = Action(increment, {'counter': tools['счетчик']})

conditions.append(Condition(
    BinaryEventChain(None, events['dkljfa'], None),
    [actions['dkdkkd']]
))
