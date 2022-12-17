""" This class is really only necessary for running the video on the desktop,
I'll either rewrite it into some sort of controller or delete it entirely later
"""
import cv2
from ..analytics import Analyzer


class VideoHandler:
    def __init__(self):
        self._capture = cv2.VideoCapture('resources/videoplayback.mp4')
        self.frame_width = None if not self._capture.isOpened() else int(self._capture.get(3))
        self.frame_height = None if not self._capture.isOpened() else int(self._capture.get(4))
        self._analyzer = Analyzer()

    def run(self):
        if not self._capture.isOpened():
            print('error opening video')
            return

        while self._capture.isOpened():
            success, frame = self._capture.read()
            if success:
                self._analyzer.process_frame(frame)
                cv2.imshow('output', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    print('interrupted')
                    break
            else:
                print('reached video end')
                break

    def __del(self):
        self._capture.release()
        cv2.destroyAllWindows()
