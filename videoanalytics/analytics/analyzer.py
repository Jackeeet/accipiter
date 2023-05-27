import queue

from . import declared
from videoanalytics.detection import ObjectDetector
from videoanalytics.models import Tracked, Detected, Coords, TrackedState
from videoanalytics.analytics.tools.abstract import Markup
from ..models.tracked_state_helpers import disappeared


class Analyzer:
    def __init__(self):
        self.detector = ObjectDetector()
        self.object_pool = dict()
        self.active = False
        self.alerts_queue = queue.Queue()
        self._timers = []

    def process_frame(self, frame):
        if not self.active:
            return frame

        detected = [o for o in self.detector.return_objects(frame)
                    if o.name in declared.object_kinds]

        if len(detected) > 0:
            markup = [tool for tool in declared.tools.values() if isinstance(tool, Markup)]
            self.object_pool = self.update_pool(self.object_pool, detected, markup)

            # print('------------------------')
            # for item in self.object_pool.values():
            #     print(item)
            #     print(f"States: {item.states}")
            #     print(f"Timers: {item.timers}")

            for tracked in self.object_pool.values():
                # checking all declared conditions
                for condition in declared.conditions:
                    # executing declared actions if the condition holds
                    if condition.condition.evaluate(tracked=tracked):
                        for action in condition.actions:
                            action.params['tracked'] = tracked
                            # action.execute()
                            action.execute(self.alerts_queue)

                # drawing the box
                tracked.obj.draw(frame)

            # drawing all declared tools
            for name, tool in declared.tools.items():
                tool.draw_on(frame)

        return frame

    @staticmethod
    def previous_position(
            pt: Coords, pool: dict[Coords, Tracked], margin: int
    ) -> Coords | None:
        for point in pool.keys():
            if abs(point.x - pt.x) <= margin and abs(point.y - pt.y) <= margin:
                return point

        return None

    @staticmethod
    def update_pool(
            pool: dict[Coords, Tracked], objects: list[Detected], markup: list[Markup]
    ) -> dict[Coords, Tracked]:
        margin = 50

        pool = {coords: tracked for coords, tracked in pool.items() if not disappeared(tracked)}
        for tracked_object in pool.values():
            tracked_object.FTL -= 1
            if tracked_object.FTL > 0:
                tracked_object.states[markup[0]] &= ~TrackedState.NEW
            else:
                tracked_object.states[markup[0]] |= TrackedState.DISAPPEARED

        for detected_object in objects:
            corner = detected_object.box.start
            if corner not in pool.keys():
                prev_corner = Analyzer.previous_position(corner, pool, margin)
                if prev_corner:
                    # the object is already tracked, and it moved
                    tracked = pool.pop(prev_corner)
                    tracked.FTL = Tracked.max_FTL
                    tracked.obj = detected_object
                else:
                    # the object is not tracked yet
                    tracked = Tracked(detected_object, markup)
            else:
                # the object is tracked, and it hadn't moved
                tracked = pool[corner]
                tracked.FTL = Tracked.max_FTL

            pool[corner] = tracked

        return {pt: obj for pt, obj in pool.items() if obj.FTL >= 0}
