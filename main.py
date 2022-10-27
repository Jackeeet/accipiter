import cv2
from support.checkers import segments_intersect
from support.primitives import Segment, Point, Text
from support.detected_object import Detected, Tracked
import object_detector as det

DEBUG_detected_count = 0
DEBUG_tracked_count = 0


def draw_bounding_box(image, label, box, color=123) -> None:
    label = str(label)
    cv2.rectangle(image, (box.start.x, box.start.y),
                  (box.start.x + box.width, box.start.y + box.height), color, 2)
    cv2.putText(image, label, (box.start.x - 10, box.start.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def intersects(tracked: Tracked, seg: Segment) -> bool:
    b = tracked.obj.box
    diag1 = Segment(b.start, Point(b.start.x + b.width, b.start.y + b.height))
    diag2 = Segment(Point(b.start.x + b.width, b.start.y),
                    Point(b.start.x, b.start.y + b.height))

    return segments_intersect(diag1, seg) or segments_intersect(diag2, seg)


def previous_position(pt: Point, pool: dict[Point, Tracked], margin: int) -> Point:
    for point in pool.keys():
        if abs(point.x - pt.x) <= margin and abs(point.y - pt.y) <= margin:
            return point

    return None


def update_pool(pool: dict[Point, Tracked], objects: list[Detected]) -> dict[Point, Tracked]:
    margin = 10
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
                pool[corner] = Tracked(det_obj)
                global DEBUG_tracked_count
                DEBUG_tracked_count += 1
        else:
            pool[corner].FTL = pool[corner].max_FTL

    return {pt: obj for pt, obj in pool.items() if obj.FTL > 0}


if __name__ == "__main__":
    detector = det.ObjectDetector()
    cap = cv2.VideoCapture('resources/videoplayback.mp4')

    if not cap.isOpened():
        print('error opening video')
    else:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        segment_x = int(frame_width * 1 / 3)
        segment = Segment(Point(segment_x, 0),
                          Point(segment_x, frame_height), color=(0, 0, 255))

        number = Text((frame_width - 70, frame_height - 10))

        count = 0
        pool = dict()   # all objects on screen

        while cap.isOpened():
            success, frame = cap.read()
            if success:
                detected = [o for o in detector.return_objects(
                    frame) if o.name == 'person']

                DEBUG_detected_count += len(detected)

                pool = update_pool(pool, detected)

                for tracked in pool.values():
                    if tracked.FTL != tracked.max_FTL:
                        continue    # don't draw boxes from previous frames

                    if intersects(tracked, segment):
                        count += 1
                        draw_bounding_box(frame, tracked.obj.name,
                                          tracked.obj.box, color=48)
                    else:
                        draw_bounding_box(
                            frame, tracked.obj.name, tracked.obj.box)

                segment.draw_on(frame)
                number.draw_on(frame, str(count))

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
