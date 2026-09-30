import conf
import dataPreProcessing as dpp
import wordCutter as wc
import pinyinGenerator as pg
import preTrainingModelApp as ptma
from sklearn.model_selection import train_test_split
from sklearn import metrics
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping
import txtReader
import numpy as np
import io
import os
import sys
import shutil
# 模型应用

# 数据集划分


def dataPartitioning(X, y):
    X1, X2, y1, y2 = train_test_split(
        X, y, test_size=0.33, random_state=42)
    return X1, X2, y1, y2

# 训练RNN080


def RNN080Training():
    # 数据预处理
    conf.logger.info('preProcessing')
    X, yOnehot, yOrigin = dpp.preProcessing()
    conf.logger.info('preProcessing end')
    # 数据集划分
    conf.logger.info('dataPartitioning')
    X1, X2, y1, y2 = dataPartitioning(X, yOnehot)
    conf.logger.info('dataPartitioning end')
    # 模型训练
    conf.logger.info("RNN080Training")
    # params
    x1Arr = np.array(X1)
    num_inputs = x1Arr.shape[1]
    input_size = x1Arr.shape[2]
    num_classes = 2
    hidden_size = 128
    learning_rate = 0.001
    num_epochs = conf.rnnEpochs
    display_step = 1
    # structure
    input_data = tf.placeholder(tf.float32, [None, num_inputs, input_size])
    targets = tf.placeholder(tf.float32, [None, num_classes])
    cell = tf.contrib.rnn.BasicRNNCell(num_units=hidden_size)
    outputs, states = tf.nn.dynamic_rnn(cell, input_data, dtype=tf.float32)
    logits = tf.layers.dense(states, num_classes)
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        labels=targets, logits=logits))
    optimizer = tf.train.AdamOptimizer(
        learning_rate=learning_rate).minimize(loss)
    # Training&Evaluating
    bestAccEpoch = 0
    maxAcc = 0
    bestRec0Epoch = 0
    maxRec0 = 0
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(num_epochs):
            # 模型训练 损失计算
            _, loss_value = sess.run([optimizer, loss], feed_dict={
                                     input_data: X1, targets: y1})
            # 模型验证
            logs = sess.run([logits], feed_dict={
                            input_data: X2, targets: y2})
            preds = tf.argmax(logs[0], axis=1).eval().tolist()
            labs = tf.argmax(y2, axis=1).eval().tolist()
            # 准确率
            acc = metrics.accuracy_score(labs, preds)
            # 查全率
            rec0 = metrics.recall_score(labs, preds, pos_label=0)
            # 更新
            if acc > maxAcc:
                bestAccEpoch = epoch
                # 保存结果
                saver.save(sess, conf.rnnModelPath+'/rnn080.ckpt')
                maxAcc = acc
            if rec0 > maxRec0:
                bestRec0Epoch = epoch
                maxRec0 = rec0
            # 训练效果分析
            if epoch % display_step == 0:
                conf.logger.info("Epoch {}: trainLoss = {},validAccuracy={:.4f},validRecall0={:.4f}".format(
                    epoch, loss_value, acc, rec0))
        conf.logger.info(
            "bestAccEpoch={},maxAcc={:.4f}".format(bestAccEpoch, maxAcc))
        conf.logger.info("bestRec0Epoch={},maxRec0={:.4f}".format(
            bestRec0Epoch, maxRec0))
    conf.logger.info("RNN080Training end")

# 测试RNN080


def RNN080Testing():
    # 分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.testpospath, conf.testnegpath)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    poswords, negwords = wc.regularing(poswords, negwords)
    conf.logger.info("Regularing end")
    # 生成标签
    conf.logger.info("genLabels")
    labels = dpp.genLabels(poswords, negwords)
    oneHotlabels = dpp.oneHotLabels(poswords, negwords)
    conf.logger.info("genLabels end")
    # 拼音嵌入
    conf.logger.info("listPinyinEmbedding")
    poswords, negwords = pg.listPinyinEmbedding(poswords, negwords)
    conf.logger.info("listPinyinEmbedding end")
    # 向量化
    conf.logger.info("listEncode")
    model = ptma.read()
    poswords, negwords = ptma.listEncode(model, poswords, negwords)
    conf.logger.info("listEncode end")
    # 整理合并
    X = poswords+negwords
    y = oneHotlabels
    y1 = labels
    # 模型加载
    # params
    num_inputs = conf.wordCountThreshold
    input_size = conf.vectorSize
    num_classes = 2
    hidden_size = 128
    learning_rate = 0.001
    num_epochs = conf.rnnEpochs
    display_step = 1
    # structure
    input_data = tf.placeholder(tf.float32, [None, num_inputs, input_size])
    targets = tf.placeholder(tf.float32, [None, num_classes])
    cell = tf.contrib.rnn.BasicRNNCell(num_units=hidden_size)
    outputs, states = tf.nn.dynamic_rnn(cell, input_data, dtype=tf.float32)
    logits = tf.layers.dense(states, num_classes)
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        labels=targets, logits=logits))
    optimizer = tf.train.AdamOptimizer(
        learning_rate=learning_rate).minimize(loss)
    # 模型评估
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, conf.rnnModelPath+'/rnn080.ckpt')
        logs = sess.run([logits], feed_dict={
            input_data: X, targets: y})
        preds = tf.argmax(logs[0], axis=1).eval().tolist()
        labs = tf.argmax(y, axis=1).eval().tolist()
        conf.logger.info('\n'+str(metrics.classification_report(labs, preds)))

# CNNCommon训练


def CNNCommonTraining():
    # 数据预处理
    conf.logger.info('preProcessing')
    X, yOnehot, yOrigin = dpp.preProcessingExPinyin()
    conf.logger.info('preProcessing end')
    # 数据集划分
    conf.logger.info('dataPartitioning')
    X1, X2, y1, y2 = dataPartitioning(X, yOrigin)
    conf.logger.info('dataPartitioning end')
    # 模型训练
    conf.logger.info('CNNCommonTraining')
    # 参数设定
    h = conf.wordCountThreshold
    w = conf.vectorSize
    X1 = np.array(X1).reshape(-1, h, w, 1).astype('float32')
    y1 = np.array(y1).astype('float32')
    X2 = np.array(X2).reshape(-1, h, w, 1).astype('float32')
    y2 = np.array(y2).astype('float32')

    # 定义模型
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                               input_shape=(h, w, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # 编译模型
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # 设置早停策略
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    # 训练模型
    model.fit(X1, y1, epochs=conf.cnnCommonEpochs, batch_size=32,
              validation_data=(X2, y2), callbacks=[early_stopping])
    # 在验证集上评估模型性能
    loss, acc = model.evaluate(X2, y2, verbose=2)
    conf.logger.info('Validation accuracy:{}'.format(acc))

    # 保存训练结果
    if os.path.exists(conf.cnnCommonModelPath):
        os.remove(conf.cnnCommonModelPath)
    model.save(conf.cnnCommonModelPath)
    conf.logger.info('CNNCommonTraining end')

# CNNCommon 测试


def CNNCommonTesting():
   # 分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.testpospath, conf.testnegpath)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    poswords, negwords = wc.regularing(poswords, negwords)
    conf.logger.info("Regularing end")
    # 生成标签
    conf.logger.info("genLabels")
    labels = dpp.genLabels(poswords, negwords)
    oneHotlabels = dpp.oneHotLabels(poswords, negwords)
    conf.logger.info("genLabels end")
    # 向量化
    conf.logger.info("listEncode")
    model = ptma.readExPinyin()
    poswords, negwords = ptma.listEncode(model, poswords, negwords)
    conf.logger.info("listEncode end")
    # 整理合并
    X = poswords+negwords
    y = oneHotlabels
    y1 = labels
    # 模型加载
    h = conf.wordCountThreshold
    w = conf.vectorSize
    X = np.array(X).reshape(-1, h, w, 1).astype('float32')
    model = load_model(conf.cnnCommonModelPath)
    # 模型评估
    loss, acc = model.evaluate(X, y1, verbose=2)
    conf.logger.info('\nloss:{}\nTest accuracy:{}'.format(loss, acc))

# 训练CNN080


def CNN080Training():
    # 数据预处理
    conf.logger.info('preProcessing')
    X, yOnehot, yOrigin = dpp.preProcessing()
    conf.logger.info('preProcessing end')
    # 数据集划分
    conf.logger.info('dataPartitioning')
    X1, X2, y1, y2 = dataPartitioning(X, yOrigin)
    conf.logger.info('dataPartitioning end')
    # 模型训练
    conf.logger.info('CNN080Training')
    # 参数设定
    h = conf.wordCountThreshold
    w = conf.vectorSize
    X1 = np.array(X1).reshape(-1, h, w, 1).astype('float32')
    y1 = np.array(y1).astype('float32')
    X2 = np.array(X2).reshape(-1, h, w, 1).astype('float32')
    y2 = np.array(y2).astype('float32')

    # 定义模型
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
                               input_shape=(h, w, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # 编译模型
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # 设置早停策略
    early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    # 训练模型
    model.fit(X1, y1, epochs=conf.cnn080Epochs, batch_size=32,
              validation_data=(X2, y2), callbacks=[early_stopping])
    # 在验证集上评估模型性能
    loss, acc = model.evaluate(X2, y2, verbose=2)
    conf.logger.info('Validation accuracy:{}'.format(acc))
    # 保存训练结果
    if os.path.exists(conf.cnn080ModelPath):
        os.remove(conf.cnn080ModelPath)
    model.save(conf.cnn080ModelPath)
    conf.logger.info('CNN080Training end')

# 测试CNN080


def CNN080Testing():
    # 分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.testpospath, conf.testnegpath)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    poswords, negwords = wc.regularing(poswords, negwords)
    conf.logger.info("Regularing end")
    # 生成标签
    conf.logger.info("genLabels")
    labels = dpp.genLabels(poswords, negwords)
    oneHotlabels = dpp.oneHotLabels(poswords, negwords)
    conf.logger.info("genLabels end")
    # 拼音嵌入
    conf.logger.info("listPinyinEmbedding")
    poswords, negwords = pg.listPinyinEmbedding(poswords, negwords)
    conf.logger.info("listPinyinEmbedding end")
    # 向量化
    conf.logger.info("listEncode")
    model = ptma.read()
    poswords, negwords = ptma.listEncode(model, poswords, negwords)
    conf.logger.info("listEncode end")
    # 整理合并
    X = poswords+negwords
    y = oneHotlabels
    y1 = labels
    # 模型加载
    h = conf.wordCountThreshold
    w = conf.vectorSize
    X = np.array(X).reshape(-1, h, w, 1).astype('float32')
    model = load_model(conf.cnn080ModelPath)
    # 模型评估
    loss, acc = model.evaluate(X, y1, verbose=2)
    conf.logger.info('\nloss:{}\nTest accuracy:{}'.format(loss, acc))

# 训练RNNCommon


def RNNCommonTraining():
    # 数据预处理
    conf.logger.info('preProcessing')
    X, yOnehot, yOrigin = dpp.preProcessingExPinyin()
    conf.logger.info('preProcessing end')
    # 数据集划分
    conf.logger.info('dataPartitioning')
    X1, X2, y1, y2 = dataPartitioning(X, yOnehot)
    conf.logger.info('dataPartitioning end')
    # 模型训练
    conf.logger.info("RNNCommonTraining")
    # params
    x1Arr = np.array(X1)
    num_inputs = x1Arr.shape[1]
    input_size = x1Arr.shape[2]
    num_classes = 2
    hidden_size = 128
    learning_rate = 0.001
    num_epochs = conf.rnnCommonEpochs
    display_step = 1
    # structure
    input_data = tf.placeholder(tf.float32, [None, num_inputs, input_size])
    targets = tf.placeholder(tf.float32, [None, num_classes])
    cell = tf.contrib.rnn.BasicRNNCell(num_units=hidden_size)
    outputs, states = tf.nn.dynamic_rnn(cell, input_data, dtype=tf.float32)
    logits = tf.layers.dense(states, num_classes)
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        labels=targets, logits=logits))
    optimizer = tf.train.AdamOptimizer(
        learning_rate=learning_rate).minimize(loss)
    # Training&Evaluating
    bestAccEpoch = 0
    maxAcc = 0
    bestRec0Epoch = 0
    maxRec0 = 0
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(num_epochs):
            # 模型训练 损失计算
            _, loss_value = sess.run([optimizer, loss], feed_dict={
                                     input_data: X1, targets: y1})
            # 模型验证
            logs = sess.run([logits], feed_dict={
                            input_data: X2, targets: y2})
            preds = tf.argmax(logs[0], axis=1).eval().tolist()
            labs = tf.argmax(y2, axis=1).eval().tolist()
            # 准确率
            acc = metrics.accuracy_score(labs, preds)
            # 查全率
            rec0 = metrics.recall_score(labs, preds, pos_label=0)
            # 更新
            if acc > maxAcc:
                bestAccEpoch = epoch
                # 保存结果
                saver.save(sess, conf.rnnCommonModelPath+'/rnnCommon.ckpt')
                maxAcc = acc
            if rec0 > maxRec0:
                bestRec0Epoch = epoch
                maxRec0 = rec0
            # 训练效果分析
            if epoch % display_step == 0:
                conf.logger.info("Epoch {}: trainLoss = {},validAccuracy={:.4f},validRecall0={:.4f}".format(
                    epoch, loss_value, acc, rec0))
        conf.logger.info(
            "bestAccEpoch={},maxAcc={:.4f}".format(bestAccEpoch, maxAcc))
        conf.logger.info("bestRec0Epoch={},maxRec0={:.4f}".format(
            bestRec0Epoch, maxRec0))
    conf.logger.info("RNNCommonTraining end")

# 测试RNNCommon


def RNNCommonTesting():
    # 分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.testpospath, conf.testnegpath)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    poswords, negwords = wc.regularing(poswords, negwords)
    conf.logger.info("Regularing end")
    # 生成标签
    conf.logger.info("genLabels")
    labels = dpp.genLabels(poswords, negwords)
    oneHotlabels = dpp.oneHotLabels(poswords, negwords)
    conf.logger.info("genLabels end")
    # 向量化
    conf.logger.info("listEncode")
    model = ptma.readExPinyin()
    poswords, negwords = ptma.listEncode(model, poswords, negwords)
    conf.logger.info("listEncode end")
    # 整理合并
    X = poswords+negwords
    y = oneHotlabels
    y1 = labels
    # 模型加载
    # params
    num_inputs = conf.wordCountThreshold
    input_size = conf.vectorSize
    num_classes = 2
    hidden_size = 128
    learning_rate = 0.001
    num_epochs = conf.rnnEpochs
    display_step = 1
    # structure
    input_data = tf.placeholder(tf.float32, [None, num_inputs, input_size])
    targets = tf.placeholder(tf.float32, [None, num_classes])
    cell = tf.contrib.rnn.BasicRNNCell(num_units=hidden_size)
    outputs, states = tf.nn.dynamic_rnn(cell, input_data, dtype=tf.float32)
    logits = tf.layers.dense(states, num_classes)
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        labels=targets, logits=logits))
    optimizer = tf.train.AdamOptimizer(
        learning_rate=learning_rate).minimize(loss)
    # 模型评估
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, conf.rnnCommonModelPath+'/rnnCommon.ckpt')
        logs = sess.run([logits], feed_dict={
            input_data: X, targets: y})
        preds = tf.argmax(logs[0], axis=1).eval().tolist()
        labs = tf.argmax(y, axis=1).eval().tolist()
        conf.logger.info('\n'+str(metrics.classification_report(labs, preds)))
