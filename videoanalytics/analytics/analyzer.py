from . import declared
from videoanalytics.detection import ObjectDetector
from videoanalytics.models import Tracked, Detected, Coords


class Analyzer:
    def __init__(self):
        self.detector = ObjectDetector()
        self.object_pool = dict()
        self.DEBUG_detected_count = 0
        self.DEBUG_tracked_count = 0

    def process_frame(self, frame):
        detected = [o for o in self.detector.return_objects(frame)
                    if o.name in declared.object_kinds]
        self.DEBUG_detected_count += len(detected)
        self.object_pool = self.update_pool(self.object_pool, detected)
        for tracked in self.object_pool.values():
            if tracked.FTL != tracked.max_FTL:
                continue  # don't process boxes from previous frames

            # checking all declared conditions
            for condition in declared.conditions:
                # executing declared actions if the condition holds
                if condition.condition.check(tracked):
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
    def previous_position(pt: Coords, pool: dict[Coords, Tracked], margin: int) -> Coords | None:
        for point in pool.keys():
            if abs(point.x - pt.x) <= margin and abs(point.y - pt.y) <= margin:
                return point

        return None

    def update_pool(self, pool: dict[Coords, Tracked], objects: list[Detected]) -> dict[Coords, Tracked]:
        margin = 50
        for point in pool.values():
            point.FTL -= 1

        for det_obj in objects:
            corner = det_obj.box.start_angle
            if corner not in pool.keys():
                prev_corner = Analyzer.previous_position(corner, pool, margin)
                # this seems a bit too complicated, there's probably a better way to do the same thing
                if prev_corner:
                    tracked = pool[prev_corner]
                    tracked.FTL = tracked.max_FTL
                    tracked.id = corner
                    tracked.obj = det_obj
                    pool.pop(prev_corner)
                    pool[corner] = tracked
                else:
                    self.DEBUG_tracked_count += 1
                    pool[corner] = Tracked(det_obj)
            else:
                pool[corner].FTL = pool[corner].max_FTL

        return {pt: obj for pt, obj in pool.items() if obj.FTL > 0}

    def __del__(self):
        print(f"DETECTED: {self.DEBUG_detected_count}")
        print(f"TRACKED: {self.DEBUG_tracked_count}")
