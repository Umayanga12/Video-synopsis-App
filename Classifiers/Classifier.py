import json
import os

import cv2
import imutils
import numpy as np
import tensorflow as tf

from Application.Classifiers.ClassifierInterface import ClassifierInterface


class Classifier(ClassifierInterface):
    def __init__(self):
        print("1")
        self.model_path = os.path.join(os.path.dirname(__file__), "./class1.pb")
        self.odapi = self.DetectorAPI(path_to_ckpt=self.model_path)
        self.threshold = 0.9
        with open(os.path.join(os.path.dirname(__file__), "coco_map.json")) as file:
            mapping = json.load(file)
            self.classes = dict()
            for element in mapping:
                self.classes[element["id"]] = element["display_name"]

    def detect(self, img):
        # get the results from the net
        boxes, scores, classes, num = self.odapi.process_frame(img)
        res = False
        for i in range(len(boxes)):
            if scores[i] > self.threshold:
                if classes[i] in self.classes:
                    # print(self.classes[classes[i]])
                    return self.classes[classes[i]]

    def tagLayer(self, data):
        res = []
        for cnts in data:
            for cnt in cnts:
                if cnt.any():
                    cv2.imshow("changes x", cnt)
                    cv2.waitKey(10) & 0xFF
                    cnt = imutils.resize(cnt, width=320)
                    x = self.detect(cnt)

                    res.append(x)

        di = dict()
        for re in res:
            if re not in di:
                di[re] = 0
            di[re] += 1

        di.pop(None, None)
        total = 0
        for value in di.values():
            total += value

        result = []
        for key, value in di.items():
            if value > len(data) / len(di) / 2:
                result.append(key)

        return result

    class DetectorAPI:
        def __init__(self, path_to_ckpt):
            self.path_to_ckpt = path_to_ckpt
            gpus = tf.config.experimental.list_physical_devices("GPU")
            if gpus:
                try:
                    for gpu in gpus:
                        tf.config.experimental.set_memory_growth(gpu, True)
                except RuntimeError as e:
                    print(e)
            self.detection_graph = tf.Graph()
            with self.detection_graph.as_default():
                od_graph_def = tf.GraphDef()
                with tf.gfile.GFile(self.path_to_ckpt, "rb") as fid:
                    serialized_graph = fid.read()
                    od_graph_def.ParseFromString(serialized_graph)
                    tf.import_graph_def(od_graph_def, name="")

            self.default_graph = self.detection_graph.as_default()
            self.sess = tf.Session(graph=self.detection_graph)

            self.image_tensor = self.detection_graph.get_tensor_by_name("image_tensor:0")
            self.detection_boxes = self.detection_graph.get_tensor_by_name("detection_boxes:0")
            self.detection_scores = self.detection_graph.get_tensor_by_name("detection_scores:0")
            self.detection_classes = self.detection_graph.get_tensor_by_name("detection_classes:0")
            self.num_detections = self.detection_graph.get_tensor_by_name("num_detections:0")

        def process_frame(self, image):
            image_np_expanded = np.expand_dims(image, axis=0)
            (boxes, scores, classes, num) = self.sess.run(
                [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
                feed_dict={self.image_tensor: image_np_expanded},
            )

            im_height, im_width, _ = image.shape
            boxes_list = [None for i in range(boxes.shape[1])]
            for i in range(boxes.shape[1]):
                boxes_list[i] = (
                    int(boxes[0, i, 0] * im_height),
                    int(boxes[0, i, 1] * im_width),
                    int(boxes[0, i, 2] * im_height),
                    int(boxes[0, i, 3] * im_width),
                )

            return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

        def close(self):
            self.sess.close()
            self.default_graph.close()
