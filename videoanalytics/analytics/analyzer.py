from . import declared
from videoanalytics.detection import ObjectDetector
from videoanalytics.models import Tracked, Detected, Coords
from videoanalytics.analytics.tools.abstract import Markup


class Analyzer:
    def __init__(self):
        self.detector = ObjectDetector()
        self.object_pool = dict()
        self.DEBUG_detected_count = 0
        self.DEBUG_tracked_count = 0
        self._timers = []

    def process_frame(self, frame):

        # todo maybe return early if no objects are detected
        detected = [o for o in self.detector.return_objects(frame)
                    if o.name in declared.object_kinds]
        # ]

        self.DEBUG_detected_count += len(detected)

        markup = [tool for tool in declared.tools.values() if isinstance(tool, Markup)]
        self.object_pool = self.update_pool(self.object_pool, detected, markup)

        print('------------------------')
        for item in self.object_pool.values():
            print(item)
            print(f"States: {item.states}")
            print(f"Timers: {item.timers}")

        for tracked in self.object_pool.values():
            # if tracked.FTL != tracked.max_FTL:
            #     continue  # don't process boxes from previous frames

            # checking all declared conditions
            for condition in declared.conditions:
                # executing declared actions if the condition holds
                if condition.condition.evaluate(tracked=tracked):
                    for action in condition.actions:
                        action.params['tracked'] = tracked
                        action.execute()

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

    def update_pool(
            self, pool: dict[Coords, Tracked], objects: list[Detected], markup: list[Markup]
    ) -> dict[Coords, Tracked]:
        margin = 50
        for point in pool.values():
            point.FTL -= 1

        for det_obj in objects:
            corner = det_obj.box.start
            if corner not in pool.keys():
                prev_corner = Analyzer.previous_position(corner, pool, margin)
                if prev_corner:
                    tracked = pool.pop(prev_corner)
                    tracked.FTL = tracked.max_FTL
                    tracked.obj = det_obj
                    # tracked.timers = {k: v for k, v in tracked.timers}
                    pool[corner] = tracked
                else:
                    self.DEBUG_tracked_count += 1
                    pool[corner] = Tracked(det_obj, markup)
            else:
                pool[corner].FTL = pool[corner].max_FTL

        return {pt: obj for pt, obj in pool.items() if obj.FTL > 0}

    def __del__(self):
        print(f"DETECTED: {self.DEBUG_detected_count}")
        print(f"TRACKED: {self.DEBUG_tracked_count}")
