#! /usr/bin/python3

"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""

import os
import io
import sys
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('img_dir', './data/', 'Path to images')
FLAGS = flags.FLAGS

# add class labels
def class_text_to_int(row_label):
    if row_label == 'apple':
        return 1
    elif row_label == "tomato":
        return 2
    elif row_label == "banana":
        return 3
    elif row_label == "pepper":
        return 4
    elif row_label == "egg":
        return 5
    elif row_label == "cucumber":
        return 6
    elif row_label == "eggplant":
        return 7
    elif row_label == "cabbage":
        return 8
    elif row_label == "chinese_cabbage":
        return 9
    elif row_label == "strawberry":
        return 10
    elif row_label == "grape":
        return 11
    elif row_label == "orange":
        return 12
    elif row_label == "lemon":
        return 13
    elif row_label == "watermelon":
        return 14
    elif row_label == "pineapple":
        return 15
    elif row_label == "carrot":
        return 16
    elif row_label == "green_onion":
        return 17
    elif row_label == "garlic":
        return 18
    elif row_label == "onion":
        return 19
    elif row_label == "ginger":
        return 20
    elif row_label == "corn":
        return 21
    elif row_label == "potato":
        return 22
    elif row_label == "sweet_potato":
        return 23
    elif row_label == "radish":
        return 24
    elif row_label == "leaf_lettuce":
        return 25
    elif row_label == "brocolli":
        return 26
    elif row_label == "white_mushroom":
        return 27
    elif row_label == "shiitake_mushroom":
        return 28
    elif row_label == "enoki_mushroom":
        return 29
    elif row_label == "asparagus":
        return 30
    elif row_label == "chilli_pepper":
        return 31
    elif row_label == "spinich":
        return 32
    elif row_label == "lettuce":
        return 33
    else:
        return -1

# return a list which is grouped by given group
def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)

    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def create_tf_record(group, path):

    if group.filename not in os.listdir(path):
        print("Could not find {}".format(group.filename))
        sys.exit(0)

    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)

    width, height = image.size

    filename = group.filename.encode('utf8')
    print(filename)
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features = tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example

def main(_):
    print("Loading TFRecordWriter ...")
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    print("TFRecordWriter Loaded!")

    print("Setting image path ...")
    path = os.path.join(FLAGS.img_dir)
    print("Image path set!")

    print("Reading csv file ...")
    img_data = pd.read_csv(FLAGS.csv_input)
    print("csv file loaded!")

    # split dataframe with filenames
    grouped = split(img_data, 'filename')

    file_errors = 0

    for group in grouped:

        try:
            tf_record = create_tf_record(group, path)
            writer.write(tf_example.SerializeToString())
        except:
            file_errors += 1

    writer.close()

    print("FINISHED. There were {} errors".format(file_errors))

    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()