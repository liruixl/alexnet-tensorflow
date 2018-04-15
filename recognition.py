import tensorflow as tf
from alexnet import AlexNet

import sys
from PIL import Image
import numpy as np
import argparse

save_path = '/home/hexiang/data/tflogs/ckpt/model_step299ckpt'

classes_name = ['折叠', '压痕', '划伤', '结疤', '氧化铁皮', '黑斑']
NUM_CLASSES = 6


def test_one_image(img_path):
    im_arr = load_and_process_one_image(img_path)
    im_tensor = tf.convert_to_tensor(im_arr)
    im_tensor = tf.reshape(im_tensor, [1, 224, 224, 1])
    im_tensor = tf.cast(im_tensor, tf.float32) * (1. / 255) - 0.5

    model = AlexNet(im_tensor, 1., NUM_CLASSES, skip_layer='')
    output = model.fc8
    logit = tf.nn.softmax(output)

    max = tf.argmax(logit, 1)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, save_path)
        print(sess.run(output))

        probable = sess.run(max)[0]

    return probable


def load_and_process_one_image(img_path, target_h=224, target_w=224):
    if not is_img(img_path):
        raise Exception('路径目标对象不是图片')

    im = Image.open(img_path)
    im = im.convert('L')
    width, height = im.size
    print(im.size)
    if height>target_h and width>target_w:
        left = (width-target_w)//2
        right = width-left
        top = (height-target_h)//2
        bottom = height-top

        # print(left, top, right, bottom)
        im1 = im.crop((left, top, right, bottom))
        # print(im1.size)
    else:
        im1 = im.resize(target_w, target_h)

    image_arr = np.array(im1)
    return image_arr


def is_img(img_path):
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', default=r'/home/hexiang/data/AllSample/train_set/2/D1_M_1457_02282.tif', type=str,
                        help='the path of image to recognition')
    args, unparsed = parser.parse_known_args()
    prob = test_one_image(args.img_path)
    print('class %d: %s'%(prob, classes_name[prob]))