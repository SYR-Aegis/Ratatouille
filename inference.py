#! /usr/bin/python3

import tensorflow as tf
import os
import cv2
import numpy as np

from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

item_map = {
    1:"사과", 2:"토마토", 3:"바나나", 4:"피망", 5:"달걀",
    6:"오이", 7:"가지", 8:"양배추", 9:"배추", 10:"딸기",
    11:"포도", 12:"오렌지", 13:"레몬", 14:"수박", 15:"파인애플",
    16:"당근", 17:"파", 18:"마늘", 19:"양파", 20:"생강",
    21:"옥수수", 22:"감자", 23:"고구마", 24:"무", 25:"상추",
    26:"브로콜리", 27:"양송이버섯", 28:"표고버섯", 29:"팽이버섯", 30:"아스파라거스",
    31:"고추", 32:"시금치", 33:"양상추"
}

PATH_TO_CKPT = "dataset/models/model/frozen_inference_graph.pb"
PATH_TO_LABELS = os.path.join("dataset/data", "labelmap.pbtxt")
NUM_CLASSES = 1

detection_graph = tf.Graph()

with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=NUM_CLASSES, use_display_name=True
)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(im_height, im_width, 3).astype(np.uint8)

def get_recipe(PATH_TO_IMG: str):

    if not os.path.isfile(PATH_TO_IMG):
        return "File not found error", 1

    recipe_url = "https://www.haemukja.com/recipes?utf8=%E2%9C%93&sort=rlv&name="

    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) as sess:
            while True:
                # read image
                img = np.array(Image.open(PATH_TO_IMG))
                
                # expand dimensions since the model expects image to have shape: [1, None, None, 3]
                img_expand = np.expand_dims(img, axis=0)

                # extract image tensor
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                #extract detection boxes
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # extract detection scores
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                # extract detection classes
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                # extract number of detections
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                # actual detection
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: img_expand}
                )

                # visualization of the results of a detection
                vis_util.visualize_boxes_and_labels_on_image_array(
                    img,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8
                )

                # display output
                cv2.imshow('obj detection', cv2.resize(img, (800,600)))
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
            
            scores.flatten()
            classes.flatten()
            
            items = list()
            
            for row, r in zip(scores, range(len(scores))):
                for score, i in zip(row, range(len(row))):
                    if score >= 0.5:
                        items.append(category_index[int(classes[r][i])]['id'])

            if len(items) == 0:
                return "Ingredient not found error", 2

            item_set = set(items)
            item_set_label = [item_map[item] for item in item_set]

            for ingredient in item_set_label:
                recipe_url += ingredient+"+"

            return recipe_url[:-1], 0

print(get_recipe("test.jpg"))