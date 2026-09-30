import dataPreProcessing as dpp
import conf
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

# 模型应用

# 加载


def load():
    # RNN080
    if conf.modelSelection == 0:
        # params
        num_inputs = conf.wordCountThreshold
        input_size = conf.vectorSize
        num_classes = 2
        hidden_size = 128
        learning_rate = 0.001
        display_step = 1
        # structure
        global input_data
        input_data = tf.placeholder(tf.float32, [None, num_inputs, input_size])
        global targets
        targets = tf.placeholder(tf.float32, [None, num_classes])
        global cell
        cell = tf.contrib.rnn.BasicRNNCell(num_units=hidden_size)
        global outputs, states
        outputs, states = tf.nn.dynamic_rnn(cell, input_data, dtype=tf.float32)
        global logits
        logits = tf.layers.dense(states, num_classes)
        return
    # CNNCommon
    if conf.modelSelection == 1:
        # 模型加载
        global hc
        hc = conf.wordCountThreshold
        global wc
        wc = conf.vectorSize
        global modelc
        modelc = load_model(conf.cnnCommonModelPath)
        return
    # CNN080
    if conf.modelSelection == 2:
        # 模型加载
        global h
        h = conf.wordCountThreshold
        global w
        w = conf.vectorSize
        global model
        model = load_model(conf.cnn080ModelPath)
        return
    # RNNCommon
    if conf.modelSelection == 3:
        # params
        num_inputs = conf.wordCountThreshold
        input_size = conf.vectorSize
        num_classes = 2
        hidden_size = 128
        learning_rate = 0.001
        display_step = 1
        # structure
        global input_datac
        input_datac = tf.placeholder(
            tf.float32, [None, num_inputs, input_size])
        global targetsc
        targetsc = tf.placeholder(tf.float32, [None, num_classes])
        global cellc
        cellc = tf.contrib.rnn.BasicRNNCell(num_units=hidden_size)
        global outputsc, statesc
        outputsc, statesc = tf.nn.dynamic_rnn(
            cellc, input_datac, dtype=tf.float32)
        global logitsc
        logitsc = tf.layers.dense(statesc, num_classes)
        return
    return

# 模型预测(输出分类标签)


def predict(X):
    # RNN080
    if conf.modelSelection == 0:
        global input_data
        global targets
        global cell
        global outputs, states
        global logits
        res = []
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, conf.rnnModelPath)
            logs = sess.run([logits], feed_dict={
                input_data: X})
            preds = tf.argmax(logs[0], axis=1).eval().tolist()
            res = preds
        return res
    # CNNCommon
    if conf.modelSelection == 1:
        global hc
        global wc
        global modelc
        res = []
        X = np.array(X).reshape(-1, hc, wc, 1).astype('float32')
        predictions = modelc.predict(X)
        for prediction in predictions:
            if prediction[0] > 0.5:
                res.append(1)
            if prediction[0] <= 0.5:
                res.append(0)
        return res
    # CNN080
    if conf.modelSelection == 2:
        global h
        global w
        global model
        res = []
        X = np.array(X).reshape(-1, h, w, 1).astype('float32')
        predictions = model.predict(X)
        for prediction in predictions:
            if prediction[0] > 0.5:
                res.append(1)
            if prediction[0] <= 0.5:
                res.append(0)
        return res
        # RNNCommon
    if conf.modelSelection == 3:
        global input_datac
        global targetsc
        global cellc
        global outputsc, statesc
        global logitsc
        res = []
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, conf.rnnCommonModelPath)
            logs = sess.run([logitsc], feed_dict={
                input_datac: X})
            preds = tf.argmax(logs[0], axis=1).eval().tolist()
            res = preds
        return res

# 模型预测(输出分类概率)


def predictProba(X):
    # RNN080
    if conf.modelSelection == 0:
        global input_data
        global targets
        global cell
        global outputs, states
        global logits
        res = []
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, conf.rnnModelPath)
            logs = sess.run([logits], feed_dict={
                input_data: X})
            probs = tf.nn.softmax(logs[0]).eval().tolist()
            res = probs
        return res
    # CNNCommon
    if conf.modelSelection == 1:
        global hc
        global wc
        global modelc
        res = []
        X = np.array(X).reshape(-1, hc, wc, 1).astype('float32')
        predictions = modelc.predict(X)
        for prediction in predictions:
            res.append([1-prediction[0], prediction[0]])
        return res
    # CNN080
    if conf.modelSelection == 2:
        global h
        global w
        global model
        res = []
        X = np.array(X).reshape(-1, h, w, 1).astype('float32')
        predictions = model.predict(X)
        for prediction in predictions:
            res.append([1-prediction[0], prediction[0]])
        return res
    # RNNCommon
    if conf.modelSelection == 3:
        global input_datac
        global targetsc
        global cellc
        global outputsc, statesc
        global logitsc
        res = []
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, conf.rnnCommonModelPath)
            logs = sess.run([logitsc], feed_dict={
                input_datac: X})
            probs = tf.nn.softmax(logs[0]).eval().tolist()
            res = probs
        return res
