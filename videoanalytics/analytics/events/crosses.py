from videoanalytics.analytics.tools.interfaces import Intersectable
from videoanalytics.models import Tracked, TrackedState, all_crossing_states, object_crossing_state, SideValue, \
    side_value_to_crossing_state
from videoanalytics.models.evaltree import EvalTree


def crosses(tracked: Tracked, tool: Intersectable, sides: EvalTree) -> bool:
    """ todo add description

    :param tracked: Отслеживаемый объект
    :param tool: элемент разметки
    :param sides:
    :return: True, если объект пересекает элемент разметки, иначе False
    """
    sides_crossing = {
        SideValue.LEFT: tool.intersects(tracked.obj.right),
        SideValue.RIGHT: tool.intersects(tracked.obj.left),
        SideValue.TOP: tool.intersects(tracked.obj.bottom),
        SideValue.BOTTOM: tool.intersects(tracked.obj.top)
    }
    new_crossing_state = object_crossing_state(sides_crossing)

    crossed = sides.evaluate(obj_crossing_state=sides_crossing)
    if sides is None:
        declared_crossing_states = all_crossing_states
    else:
        declared_crossing_states = sides.flatten(
            lambda side, initial: initial | side_value_to_crossing_state(side.value),
            TrackedState.NONE
        )

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
