from gensim.models import FastText
import wordCutter as wc
import pinyinGenerator as pg
import conf
import pickle
import shutil
import os
from datetime import datetime

# 预训练模型应用


# 预训练模型读取


def read():
    if conf.pinyinEmbed:
        model = FastText.load(conf.ptmpath)
        return model
    model = FastText.load(conf.EXPYptmpath)
    return model

# 模型应用(生成单个词对应词向量)


def encode(model, word):
    return model.wv[word].tolist()

# 模型应用(生成列表中所有词对应词向量)


def listEncode(model, wordsList):
    # 遍历语料每个词
    for words in wordsList:
        for i in range(len(words)):
            # 转化为向量
            words[i] = encode(model, words[i])
    return wordsList
