import os
import sys
from PIL import Image
import argparse
import tensorflow as tf


TFRECORDS_NAME = "/home/hexiang/data/1000/test1000.tfrecords"
IMG_HEIGHT = 1000
IMG_WIDTH = 1000
IMG_DEPTH = 1


def creat_tfrecords(data_path):
    # 使用tf.train.Example来定义我们要填入的数据格式，然后使用tf.python_io.TFRecordWriter来写入。
    writer = tf.python_io.TFRecordWriter(TFRECORDS_NAME)

    class_name_list = os.listdir(data_path)  # list of classes dirs
    print(class_name_list)
    class_name_list.sort()  # windows貌似是按照文件名字排列的, linux不是
    print(class_name_list)

    for index, class_name in enumerate(class_name_list):
        img_dir = os.path.join(data_path, class_name)
        img_name_list = os.listdir(img_dir)

        print("start %d class, directory name: %s " % (index, class_name))
        for img_name in img_name_list:
            path = os.path.join(img_dir, img_name)
            im = Image.open(path)

            if im.mode != 'L':
                print('%s is %s mode' % (img_name, im.mode))
                im = im.convert('L')
                print('convert %s to L mode' % img_name)

            box = (12, 0, 1012, 1000)
            img_crop = im.crop(box)

            # img_resized = img_crop.resize((224, 224))

            img_raw = img_crop.tobytes()  # 原生bytes
            feature = {
                "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
            }
            features = tf.train.Features(feature=feature)
            example = tf.train.Example(features=features)
            writer.write(example.SerializeToString())
        print("%d dir has DONE" % index)
    writer.close()


def read_and_decode(filename, height, width):
    # 根据文件名生成一个队列
    filename_queue = tf.train.string_input_producer([filename])  # 一个文件名list，这里只有一个tf.records的文件名

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)  # 返回文件名和文件
    # 解析器解析
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw': tf.FixedLenFeature([], tf.string),
                                       })

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [height, width, 1])
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    label = tf.cast(features['label'], tf.int32)

    return img, label


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--datapath', default=r'/home/hexiang/data/AllSample/test_set', type=str,
                        help='the dictionary of train or test data')
    # parser.add_argument('--datapath', default=r'/home/hexiang/data/AllSample/train_set', type=str, help='the dictionary of train or test data')
    args, unparsed = parser.parse_known_args()
    creat_tfrecords(args.datapath)




