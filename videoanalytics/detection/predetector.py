import os.path

from videoanalytics.models import Detected


class ObjectPredetector:
    def __init__(self, dataset):
        self.dataset = dataset
        self.folder = os.path.dirname(os.path.abspath(__file__)) + f'/predetected/{dataset}'
        self._labels_path = os.path.dirname(os.path.abspath(__file__)) + '/darknet/coco.names'
        self.frame_count = self._get_frame_count()

        with open(self._labels_path, "rt", encoding="utf-8") as labels_file:
            self.labels = labels_file.read().rstrip("\n").split("\n")

        pass

    def _get_frame_count(self):
        count = 0
        for path in os.scandir(self.folder):
            if path.is_file():
                count += 1
        return count

    def return_objects(self, frame_index):
        objects = []
        try:
            with open(f"{self.folder}/{self.dataset}_{frame_index + 1}.txt", "r") as frame:
                while line := frame.readline():
                    data = line.rstrip().split(" ")
                    label = self.labels[int(data[0])]
                    x = int(float(data[1]))
                    y = int(float(data[2]))
                    x1 = int(float(data[3]))
                    y1 = int(float(data[4]))
                    objects.append(Detected(label, 1.0, x=x, y=y, w=x1-x, h=y1-y))
        except Exception as e:
            print(e)
        finally:     
            return objects
