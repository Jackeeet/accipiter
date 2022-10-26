import cv2
from support.checkers import segments_intersect
from support.object_state import ObjectState
from support.primitives import Segment, Point, Text
from support.detected_object import DetectedObject
import object_detector as det


def draw_bounding_box(image, label, box, color=123):
    label = str(label)
    cv2.rectangle(image, (box.start.x, box.start.y),
                  (box.start.x + box.width, box.start.y + box.height), color, 2)
    cv2.putText(image, label, (box.start.x - 10, box.start.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def intersects(obj: DetectedObject, seg: Segment):
    b = obj.box
    diag1 = Segment(b.start, Point(b.start.x + b.width, b.start.y + b.height))
    diag2 = Segment(Point(b.start.x + b.width, b.start.y),
                    Point(b.start.x, b.start.y + b.height))

    return segments_intersect(diag1, seg) or segments_intersect(diag2, seg)


if __name__ == "__main__":
    detector = det.ObjectDetector()
    cap = cv2.VideoCapture('resources/videoplayback.mp4')

    if not cap.isOpened():
        print('error opening video')
    else:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        segment_x = int(frame_width * 1 / 3)
        segment = Segment(Point(segment_x, 0), Point(
            segment_x, frame_height), color=(0, 0, 255))

        number = Text((frame_width - 70, frame_height - 10))

        count = 0
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                objects = [o for o in detector.return_objects(frame) if o.name == 'person']
                for obj in objects:
                    if intersects(obj, segment):
                        # if obj.state != ObjectState.CROSSING:
                        count += 1
                        # obj.state = ObjectState.CROSSING
                        draw_bounding_box(frame, obj.name, obj.box, color=48)
                    else:
                        # obj.state = ObjectState.INACTIVE
                        draw_bounding_box(frame, obj.name, obj.box)

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
