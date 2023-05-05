from videoanalytics.analytics.tools.interfaces import Intersectable
from videoanalytics.models import SideValue, Tracked, TrackedState, all_crossing_states, Side
from videoanalytics.models.boolean import Boolean
from videoanalytics.models.evaltree import EvalTree
from videoanalytics.models.tracked_state_helpers import object_crossing_state, disappeared


def crosses(
        tracked: Tracked, tool: Intersectable, sides: EvalTree
) -> bool:
    """ todo add description

    :param tracked: Отслеживаемый объект
    :param tool: элемент разметки
    :param sides:
    :return: True, если объект пересекает элемент разметки, иначе False
    """
    if disappeared(tracked):
        return False

    if sides is None:
        sides = EvalTree(
            Side(SideValue.LEFT), 'op_or', EvalTree(
                Side(SideValue.RIGHT), 'op_or', EvalTree(
                    Side(SideValue.TOP), 'op_or', Side(SideValue.BOTTOM)
                )
            )
        )

    sides_crossing = {
        SideValue.LEFT: Boolean(tool.intersects(tracked.obj.right)),
        SideValue.RIGHT: Boolean(tool.intersects(tracked.obj.left)),
        SideValue.TOP: Boolean(tool.intersects(tracked.obj.bottom)),
        SideValue.BOTTOM: Boolean(tool.intersects(tracked.obj.top))
    }
    new_crossing_state = object_crossing_state(sides_crossing)

    def to_tracked_state_tree(side):
        if isinstance(side, Side):
            return sides_crossing[side.value]
        return side.fmap(lambda s: to_tracked_state_tree(s))

    crossed: bool = sides.fmap(lambda side: to_tracked_state_tree(side)).evaluate()
    first_crossing = False

    if crossed:
        # ни один бит в текущем состоянии не соответствует одному из битов,
        # соответствующих заданным сторонам => первое пересечение линии объектом
        if (tracked.states[tool] & sides.evaluate()) == TrackedState.NONE:
            first_crossing = True

        tracked.states[tool] |= new_crossing_state
    else:  # reset all crossing flags for this tool
        # todo make sure this doesn't erase unnecessary states
        tracked.states[tool] = tracked.states[tool] & ~all_crossing_states

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return crossed and first_crossing
