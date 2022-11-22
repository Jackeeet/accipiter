import cv2
import declared
from declarable import Coords
from support.detected_object import Detected, Tracked
from detectors.object_detector import ObjectDetector

DEBUG_detected_count = 0
DEBUG_tracked_count = 0


def previous_position(pt: Coords, pool: dict[Coords, Tracked], margin: int) -> Coords:
    for point in pool.keys():
        if abs(point.x - pt.x) <= margin and abs(point.y - pt.y) <= margin:
            return point

    return None


def update_pool(pool: dict[Coords, Tracked], objects: list[Detected]) -> dict[Coords, Tracked]:
    margin = 50
    for point in pool.values():
        point.FTL -= 1

    for det_obj in objects:
        corner = det_obj.box.start
        if corner not in pool.keys():
            prev_corner = previous_position(corner, pool, margin)
            # this seems a bit too complicated, there's probably a better way to do the same thing
            if prev_corner:
                tracked = pool[prev_corner]
                tracked.FTL = tracked.max_FTL
                tracked.id = corner
                tracked.obj = det_obj
                pool.pop(prev_corner)
                pool[corner] = tracked
            else:
                global DEBUG_tracked_count
                DEBUG_tracked_count += 1
                pool[corner] = Tracked(det_obj)
                # pool[corner].num = DEBUG_tracked_count
        else:
            pool[corner].FTL = pool[corner].max_FTL

    return {pt: obj for pt, obj in pool.items() if obj.FTL > 0}


if __name__ == "__main__":
    detector = ObjectDetector()
    cap = cv2.VideoCapture('resources/videoplayback.mp4')

    if not cap.isOpened():
        print('error opening video')
    else:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        pool = dict()   # all objects on screen

        while cap.isOpened():
            success, frame = cap.read()
            if success:
                detected = [o for o in detector.return_objects(frame)
                            if o.name in declared.object_kinds]

                DEBUG_detected_count += len(detected)
                pool = update_pool(pool, detected)

                for tracked in pool.values():
                    if tracked.FTL != tracked.max_FTL:
                        continue    # don't process boxes from previous frames

                    # checking all declared conditions
                    for condition in declared.conditions:
                        # executing declared actions if the condition holds
                        if condition.condition.check(tracked):
                            for action in condition.actions:
                                action.params['object'] = tracked
                                action.execute()

                    # drawing the box
                    tracked.obj.draw(frame)

                # drawing all declared tools
                for name, tool in declared.tools.items():
                    tool.draw_on(frame)

                cv2.imshow('output', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    print('interrupted')
                    break
            else:
                print('reached video end')
                break

        cap.release()
        cv2.destroyAllWindows()
        print(f"DETECTED: {DEBUG_detected_count}")
        print(f"TRACKED: {DEBUG_tracked_count}")
