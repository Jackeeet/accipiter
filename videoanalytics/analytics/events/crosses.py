from videoanalytics.analytics.tools.interfaces import Intersectable
from videoanalytics.models import SideValue, Tracked, TrackedState, Side
from videoanalytics.models.boolean import Boolean
from videoanalytics.models.evaltree import EvalTree
from videoanalytics.models.tracked_state_helpers import object_crossing_state, disappeared


def crosses(
        tracked: Tracked, tools: Intersectable, sides: EvalTree
) -> bool:
    """

    :param tracked: Отслеживаемый объект
    :param tools: элемент разметки
    :param sides:
    :return: True, если объект пересекает элемент разметки, иначе False
    """
    if disappeared(tracked):
        return False

    if tools.start.x == tools.end.x and (tools.start.y == 0 and tools.end.y == 464):
        actual_tool = tools.extend_y(1000)
    elif tools.start.y == tools.end.y and (tools.start.y == 0 and tools.start.y == 848):
        actual_tool = tools.extend_x(1000)
    else:
        actual_tool = tools

    if sides is None:
        sides = EvalTree(
            Side(SideValue.LEFT), 'op_or', EvalTree(
                Side(SideValue.RIGHT), 'op_or', EvalTree(
                    Side(SideValue.TOP), 'op_or', Side(SideValue.BOTTOM)
                )
            )
        )

    sides_crossing = {
        SideValue.LEFT: Boolean(actual_tool.intersects(tracked.obj.right)),
        SideValue.RIGHT: Boolean(actual_tool.intersects(tracked.obj.left)),
        SideValue.TOP: Boolean(actual_tool.intersects(tracked.obj.bottom)),
        SideValue.BOTTOM: Boolean(actual_tool.intersects(tracked.obj.top))
    }
    new_crossing_state = object_crossing_state(sides_crossing)

    def to_tracked_state_tree(side):
        if isinstance(side, Side):
            return sides_crossing[side.value]
        return side.fmap(lambda s: to_tracked_state_tree(s))

    crossed: Boolean
    if isinstance(sides, Side):
        crossed = sides_crossing[sides.value]
    else:
        crossed = sides.fmap(lambda side: to_tracked_state_tree(side)).evaluate()
    first_crossing = False

    if crossed.value:
        # ни один бит в текущем состоянии не соответствует одному из битов,
        # соответствующих заданным сторонам => первое пересечение линии объектом
        if (tracked.states[tools] & sides.evaluate()) == TrackedState.NONE:
            first_crossing = True

        tracked.states[tools] |= new_crossing_state

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return crossed.value and first_crossing
