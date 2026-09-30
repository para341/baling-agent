import sys
import conf
from datetime import datetime
import wordCutter as wc
import pinyinGenerator as pg
import preTrainingModelApp as ptma

# 生成标签


def genLabels(poswords, negwords):
    labels = [1 for i in range(len(poswords))] + \
        [0 for i in range(len(negwords))]
    return labels

# 生成独热编码标签


def oneHotLabels(poswords, negwords):
    labels = [[0, 1] for i in range(len(poswords))]+[[1, 0]
                                                     for i in range(len(negwords))]
    return labels

# 整体流程


def preProcessing():
    # 分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.pospath, conf.negpath)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    poswords, negwords = wc.regularing(poswords, negwords)
    conf.logger.info("Regularing end")
    # 生成标签
    conf.logger.info("genLabels")
    labels = genLabels(poswords, negwords)
    oneHotlabels = oneHotLabels(poswords, negwords)
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
    return X, y, y1

# 整理流程(无拼音嵌入)


def preProcessingExPinyin():
    # 分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.pospath, conf.negpath)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    poswords, negwords = wc.regularing(poswords, negwords)
    conf.logger.info("Regularing end")
    # 生成标签
    conf.logger.info("genLabels")
    labels = genLabels(poswords, negwords)
    oneHotlabels = oneHotLabels(poswords, negwords)
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
    return X, y, y1
