
import os
import tensorflow as tf
from datetime import  datetime
from alexnet import  AlexNet
from tfrecord_generator import read_and_decode

'''
Configuration setting
'''

# image info
IMG_HEIGHT = 300
IMG_WIDTH = 300
IMG_DEPTH = 1

# learning params
learning_rate = 0.001
num_epochs = 300
batch_size = 5

# Network params
dropout_rate = 0.8
num_classes = 6  # 1-折叠 2-压痕 3-划伤 4-结疤 5-氧化铁皮 6-黑斑
MAX_STEP = 3000
train_layers = ['conv1','conv2', 'conv3', 'conv4', 'conv5','fc8', 'fc7', 'fc6']

# How often we want to write the tf.summary data to disk
display_step = 10

is_use_ckpt = False
ckpt_path = '/home/hexiang/data/tflogs/ckpt/model_step299ckpt'

filewriter_path = '/home/hexiang/data/tflogs/tensorboard300'
checkpoint_path = '/home/hexiang/data/tflogs/ckpt300'
records_train_path = '/home/hexiang/data/1000/train1000.tfrecords'
records_test_path = '/home/hexiang/data/1000/test1000.tfrecords'


if not os.path.isdir(checkpoint_path):
    os.mkdir(checkpoint_path)
if not os.path.isdir(filewriter_path):
    os.mkdir(filewriter_path)

# TF placeholder for graph input and output
x = tf.placeholder(tf.float32, [batch_size, IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH])
y = tf.placeholder(tf.int32, [batch_size])
keep_prop = tf.placeholder(tf.float32)

model = AlexNet(x, keep_prop, num_classes, train_layers)

logits = model.fc8

# the list of trainable variables of the layers we want to train
var_list = [v for v in tf.trainable_variables() if v.name.split('/')[0] in train_layers]
print('训练:')
print(var_list)

with tf.name_scope('cross_ent'):
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits, name='xentropy')
    loss = tf.reduce_mean(cross_entropy, name='xent_mean')

# Train Op
with tf.name_scope('train'):
    gradients = tf.gradients(ys=loss, xs=var_list)
    gradients = list(zip(gradients, var_list))
    print('梯度:')
    print(gradients)

    # Creat optimizer and apply gradient descent to the trainable variables
    optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.9)
    #train_op = optimizer.apply_gradients(grads_and_vars=gradients)
    #optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_op = optimizer.minimize(loss)

# 梯度的直方图
for gradient, var in gradients:
    tf.summary.histogram(var.name + '/gradient', gradient)

tf.summary.scalar('cross_entropy', loss)


# evaluation op...............................................
with tf.name_scope('accuracy'):
    #correct_pred = tf.equal(tf.argmax(logits, 1), tf.to_int64(y))
    #accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    correct = tf.nn.in_top_k(logits, y, 1)
    accuracy = tf.reduce_sum(tf.cast(correct, tf.int32))
tf.summary.scalar('accuracy', accuracy)

merged_summary_op = tf.summary.merge_all()

# initialize the FileWriter
writer = tf.summary.FileWriter(filewriter_path)

saver = tf.train.Saver()

# 训练集
img, label = read_and_decode(records_train_path, IMG_HEIGHT, IMG_WIDTH)
# 使用shuffle_batch可以随机打乱输入
# capacity是队列的长度
# min_after_dequeue是出队后，队列至少剩下min_after_dequeue个数据
img_batch, label_batch = tf.train.shuffle_batch([img, label],
                                                batch_size=batch_size, capacity=3000,
                                                min_after_dequeue=10)
# 测试集
img_test, label_test = read_and_decode(records_test_path, IMG_HEIGHT, IMG_WIDTH)
img_test_batch, label_test_batch = tf.train.shuffle_batch([img_test, label_test],
                                                                    batch_size=batch_size, capacity=500,
                                                                    min_after_dequeue=10)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print('initialize all global variables')

    writer.add_graph(sess.graph)
    # summary_writer = tf.summary.FileWriter(train_event_dir, sess.graph) 也可以写在这里

    if is_use_ckpt is True:
        # 路径未定义
        saver.restore(sess, ckpt_path)
        print('Restore from checkpoint...')
    else:
        model.load_initial_weights(sess)
        print('Load the pretrained weigths into the non-trainable layer')

    coord = tf.train.Coordinator()
    thread = tf.train.start_queue_runners(sess=sess, coord=coord)

    print('{} Start training'.format(datetime.now()))
    for step in range(MAX_STEP):
        train_batch_data, train_batch_labels = sess.run([img_batch, label_batch])
        print(train_batch_data.shape, train_batch_labels)

        print('step %d starts' % step)
        start_time = datetime.now()
        _, train_loss = sess.run([train_op, loss], feed_dict={x: train_batch_data,
                                      y: train_batch_labels,
                                      keep_prop: dropout_rate})

        duration = datetime.now() - start_time

        if step%display_step == 0:
            s = sess.run(merged_summary_op, feed_dict={x: train_batch_data,
                                          y: train_batch_labels,
                                          keep_prop: 1})
            writer.add_summary(s, step)

        print('%s: step %d, loss = %.4f (%s seconds)' % (datetime.now(), step, train_loss, duration))

        if (step+1)%300 == 0 or step+1 == MAX_STEP:

            print('{} Saving checkpoint of model...'.format(datetime.now()))
            checkpoint_name = os.path.join(checkpoint_path, 'model_step' + str(step) + 'ckpt')
            save_path = saver.save(sess, checkpoint_name)
            print('{} Model checkpoint is saved at {}'.format(datetime.now(), checkpoint_name))

            print('Test the model on the entire test_set')
            test_correct = 0
            test_count = 0

            for _ in range(50):  # 500图片
                test_batch_data, test_batch_labels = sess.run([img_test_batch, label_test_batch])

                acc = sess.run(accuracy, feed_dict={x: test_batch_data,
                                                   y: test_batch_labels,
                                                   keep_prop: 1.})
                test_correct += acc
                test_count += 10
            test_acc = float(test_correct)/test_count
            print('All examples: %d Correct: %d test accuracy = %.4f' % (test_count, test_correct, test_acc))


    coord.request_stop()
    coord.join(thread)
    print('End of training')

