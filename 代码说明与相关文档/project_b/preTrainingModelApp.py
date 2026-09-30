from gensim.models import FastText
import wordCutter as wc
import pinyinGenerator as pg
import conf
import pickle
import shutil
import os
from datetime import datetime

# 预训练模型应用


# 模型训练
def preTraining():
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.pospath, conf.negpath)
    conf.logger.info("wordCutting end")

    conf.logger.info("wordEmbedding")
    poswords, negwords = pg.listPinyinEmbedding(poswords, negwords)
    conf.logger.info("wordEmbedding end")

    conf.logger.info("preTraining")
    model = FastText(poswords+negwords,  size=conf.vectorSize, window=3, min_count=1,
                     iter=10, min_n=3, max_n=6, word_ngrams=0)
    conf.logger.info("preTraining end")

    conf.logger.info("Saving")
    shutil.rmtree(conf.mparent)
    os.mkdir(conf.mparent)
    model.save(conf.ptmpath)
    conf.logger.info("Saving end")

# 模型训练(无拼音向量)


def preTrainingExPinyin():
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.pospath, conf.negpath)
    conf.logger.info("wordCutting end")

    conf.logger.info("preTraining")
    model = FastText(poswords+negwords,size=conf.vectorSize, window=3, min_count=1,
                     iter=10, min_n=3, max_n=6, word_ngrams=0)
    conf.logger.info("preTraining end")

    conf.logger.info("Saving")
    if os.path.exists(conf.EXPYmparent):
        shutil.rmtree(conf.EXPYmparent)
    os.mkdir(conf.EXPYmparent)
    model.save(conf.EXPYptmpath)
    conf.logger.info("Saving end")


# 预训练模型读取


def read():
    model = FastText.load(conf.ptmpath)
    return model

# 预训练模型读取(无拼音嵌入)


def readExPinyin():
    model = FastText.load(conf.EXPYptmpath)
    return model

# 模型应用(生成单个词对应词向量)


def encode(model, word):
    return model.wv[word].tolist()

# 模型应用(生成列表中所有词对应词向量)


def listEncode(model, poswords, negwords):
    # 遍历积极语料每个词
    for words in poswords:
        for i in range(len(words)):
            # 转化为向量
            words[i] = encode(model, words[i])
    # 遍历消极语料中每个词
    for words in negwords:
        for i in range(len(words)):
            # 转化为向量
            words[i] = encode(model, words[i])
    return poswords, negwords
