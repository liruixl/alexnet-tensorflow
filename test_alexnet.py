
import os
import tensorflow as tf
from datetime import  datetime
from alexnet import  AlexNet
from tfrecord_generator import read_and_decode

'''
Configuration setting
'''

# image info
IMG_HEIGHT = 1000
IMG_WIDTH = 1000
IMG_DEPTH = 1

# learning params
learning_rate = 0.01
num_epochs = 300
batch_size = 10

# Network params
dropout_rate = 0.5
num_classes = 6  # 0-折叠 2-压痕 3-划伤 4-结疤 5-氧化铁皮 6-黑斑
MAX_STEP = 300
train_layers = ['fc8', 'fc7', 'fc6']

# How often we want to write the tf.summary data to disk
display_step = 10

is_use_ckpt = False

filewriter_path = '/tmp/tensorboard'
checkpoint_path = '/tmp/'
records_train_path = '/home/hexiang/data/1000/train1000.tfrecords'
records_test_path = '/home/hexiang/data/1000/test1000.tfrecords'
ckpt_path = '/tmp/'

if not os.path.isdir(checkpoint_path):
    os.mkdir(checkpoint_path)

# TF placeholder for graph input and output
x = tf.placeholder(tf.float32, [batch_size, 224, 224, 1])
y = tf.placeholder(tf.int32, [batch_size])
keep_prop = tf.placeholder(tf.float32)

model = AlexNet(x, keep_prop, num_classes, train_layers)

inputs = tf.random_uniform([10, 224, 224, 1])
labels = tf.random_uniform([10])


conv1 = model.conv1
pool1 = model.pool1

conv2 = model.conv2
pool2 = model.pool2

conv3 = model.conv3

conv4 = model.conv4

conv5 = model.conv5
pool5 = model.pool5
logits = model.fc8


init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print('initialize all global variables')

    xx, yy = sess.run([inputs, labels])

    p, l = sess.run([pool5, logits], feed_dict={x: xx,
                                          y: yy,
                                          keep_prop: 1})

    print(conv1,pool1)
    print(conv2,pool2)

    print(conv3)
    print(conv4)

    print(pool5, logits)
    print(l)
