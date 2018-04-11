
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
num_epochs = 10
batch_size = 10

# Network params
dropout_rate = 0.5
num_classes = 6  # 0-折叠 2-压痕 3-划伤 4-结疤 5-氧化铁皮 6-黑斑
train_layers = ['fc8', 'fc7', 'fc6']

# How often we want to write the tf.summary data to disk
display_step = 1

is_use_ckpt = False

filewriter_path = '/tmp/tensorboard'
checkpoint_path = '/tmp/'
records_train_path = '/home/hexiang/data/1000/train1000.tfrecords'
records_test_path = '/home/hexiang/data/1000/test1000.tfrecords'
ckpt_path =''

if not os.path.isdir(checkpoint_path):
    os.mkdir(checkpoint_path)

# TF placeholder for graph input and output
x = tf.placeholder(tf.float32, [batch_size, 1000, 1000, 1])
y = tf.placeholder(tf.int32, [batch_size])
keep_prop = tf.placeholder(tf.float32)

model = AlexNet(x, keep_prop, num_classes, train_layers)

logits = model.fc8

# the list of trainable variables of the layers we want to train
var_list = [v for v in tf.trainable_variables() if v.name.split('/')[0] in train_layers]

with tf.name_scope('cross_ent'):
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits, name='xentropy')
    loss = tf.reduce_mean(cross_entropy, name='xent_mean')

# Train Op
with tf.name_scope('train'):
    gradients = tf.gradients(ys=loss, xs=var_list)
    gradients = list(zip(gradients, var_list))

# Creat optimizer and apply gradient descent to the trainable variables
optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.9)
train_op = optimizer.apply_gradients(grads_and_vars=gradients)

# 梯度的直方图
for gradient, var in gradients:
    tf.summary.histogram(var.name + '/gradient', gradient)

tf.summary.scalar('cross_entropy', loss)


# evaluation op
with tf.name_scope('accuracy'):
    correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 0))
    accurcy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
tf.summary.scalar('accuracy', accurcy)

merged_summary_op = tf.summary.merge_all()

# initialize the FileWriter
writer = tf.summary.FileWriter(filewriter_path)

saver = tf.train.Saver()

img, label = read_and_decode(records_train_path, IMG_HEIGHT, IMG_WIDTH)
# 使用shuffle_batch可以随机打乱输入
# capacity是队列的长度
# min_after_dequeue是出队后，队列至少剩下min_after_dequeue个数据
img_batch, label_batch = tf.train.shuffle_batch([img, label],
                                                batch_size=batch_size, capacity=100,
                                                min_after_dequeue=10)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print('initialize all global variables')

    writer.add_graph(sess.graph)
    # summary_writer = tf.summary.FileWriter(train_event_dir, sess.graph)

    if is_use_ckpt is True:
        # 路径未定义
        saver.restore(sess, ckpt_path)
        print('Restore from checkpoint...')
    else:
        model.load_initial_weights(sess)
        print('Load the pretrained weigths into the non-trainable layer')

    print('Start training')



