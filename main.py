import cv2
import object as obj
import object_detector as det


def draw_bounding_box(image, label, box):
    label = str(label)
    color = 123
    cv2.rectangle(image, (box.x, box.y),
                  (box.x + box.width, box.y + box.height), color, 2)
    cv2.putText(image, label, (box.x - 10, box.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


if __name__ == "__main__":
    detector = det.ObjectDetector()

    cap = cv2.VideoCapture('resources/videoplayback.mp4')
    if not cap.isOpened():
        print('error opening video')

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            objects = detector.return_objects(frame)
            for obj in objects:
                draw_bounding_box(frame, obj.name, obj.box)

            cv2.imshow('output', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                print('interrupted')
                break
        else:
            print('reached video end')
            break

    cap.release()
    cv2.destroyAllWindows()
