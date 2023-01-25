from videoanalytics.analytics.declarable.tools.interfaces import Intersectable
from videoanalytics.models import Tracked, TrackedState, crossing_states, get_crossing_state


def crosses(tracked: Tracked, tool: Intersectable) -> bool:
    """ todo add description

    :param tracked: Отслеживаемый объект
    :param tool: элемент разметки
    :return: True, если объект пересекает элемент разметки, иначе False
    """
    crossed_left = tool.intersects(tracked.obj.left)
    crossed_right = tool.intersects(tracked.obj.right)
    crossed_top = tool.intersects(tracked.obj.top)
    crossed_bottom = tool.intersects(tracked.obj.bottom)

    new_state = get_crossing_state(crossed_bottom, crossed_left, crossed_right, crossed_top)
    crossed = (new_state & crossing_states) != TrackedState.NONE
    first_crossing = False

    if not crossed:
        # reset all crossing flags for this tool
        tracked.states[tool] = tracked.states[tool] & ~crossing_states
    else:
        if (tracked.states[tool] & crossing_states) == TrackedState.NONE:
            # первое пересечение линии объектом
            first_crossing = True
        tracked.states[tool] |= new_state

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return crossed and first_crossing
