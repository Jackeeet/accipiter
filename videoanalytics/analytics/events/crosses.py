from videoanalytics.analytics.tools.interfaces import Intersectable
from videoanalytics.models import ParametrizedBool, SideValue, Tracked, TrackedState, all_crossing_states
from videoanalytics.models.boolean import Boolean
from videoanalytics.models.evaltree import EvalTree
from videoanalytics.models.tracked_state_helpers import object_crossing_state


def crosses(
        tracked: Tracked, tool: Intersectable, sides: EvalTree
) -> ParametrizedBool:
    """ todo add description

    :param tracked: Отслеживаемый объект
    :param tool: элемент разметки
    :param sides:
    :return: True, если объект пересекает элемент разметки, иначе False
    """
    declared_crossing_states: TrackedState
    declared_crossing_states = all_crossing_states if sides is None else sides.evaluate()

    sides_crossing = {
        SideValue.LEFT: Boolean(tool.intersects(tracked.obj.right)),
        SideValue.RIGHT: Boolean(tool.intersects(tracked.obj.left)),
        SideValue.TOP: Boolean(tool.intersects(tracked.obj.bottom)),
        SideValue.BOTTOM: Boolean(tool.intersects(tracked.obj.top))
    }
    new_crossing_state = object_crossing_state(sides_crossing)

    crossed: bool = sides.fmap(lambda side: sides_crossing[side.value]).evaluate().value
    first_crossing = False

    if crossed:
        # ни один бит в текущем состоянии не соответствует одному из битов,
        # соответствующих заданным сторонам => первое пересечение линии объектом
        if (tracked.states[tool] & declared_crossing_states) == TrackedState.NONE:
            first_crossing = True

        tracked.states[tool] |= new_crossing_state
    else:  # reset all crossing flags for this tool
        # todo make sure this doesn't erase unnecessary states
        tracked.states[tool] = tracked.states[tool] & ~all_crossing_states

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return crossed and first_crossing
