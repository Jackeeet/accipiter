import cv2
import numpy as np
import configparser
import object

from cv2.dnn import (
    DNN_BACKEND_CUDA,
    DNN_BACKEND_DEFAULT,
    DNN_BACKEND_OPENCV,
    DNN_TARGET_CPU,
    DNN_TARGET_CUDA,
    DNN_TARGET_OPENCL,
)


class ObjectDetector:
    def __init__(self, config=None, weights=None, labels=None):
        self.nms = 0.4
        self.confidence = 0.5
        # self.backend = DNN_BACKEND_OPENCV
        # self.target = DNN_TARGET_CPU
        self.backend = DNN_BACKEND_CUDA
        self.target = DNN_TARGET_CUDA

        self._config_path = config or 'detectors/models/darknet/yolov3.cfg'
        self._weights_path = weights or 'detectors/models/darknet/yolov3.weights'
        self._labels_path = labels or 'detectors/models/darknet/coco.names'

        with open(self._labels_path, "rt", encoding="utf-8") as labels_file:
            self.labels = labels_file.read().rstrip("\n").split("\n")

        self._setup_net()
        self._setup_model()

    def _setup_net(self):
        self.net = cv2.dnn.readNet(
            self._weights_path, self._config_path, 'darknet')
        self.net.setPreferableBackend(self.backend)
        self.net.setPreferableTarget(self.target)

    def _setup_model(self):
        model_config = configparser.ConfigParser(strict=False)
        model_config.read('detectors/models/darknet/yolov3.cfg')
        self._model_width = int(model_config.get("net", "width"))
        self._model_height = int(model_config.get("net", "height"))

        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(
            size=(self._model_width, self._model_height), scale=1 / 255)

    def return_objects(self, frame):
        labels, confidences, boxes = self.model.detect(
            frame, self.confidence, self.nms
        )

        text_labels = [self.labels[int(label)] for label in labels]
        objects = []
        for (label, confidence, box) in zip(text_labels, confidences, boxes):
            objects.append(
                object.Object(
                    label, confidence, x=box[0], y=box[1], w=box[2], h=box[3]
                )
            )

        return objects
