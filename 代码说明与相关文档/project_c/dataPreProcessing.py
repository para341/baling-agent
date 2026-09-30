import conf
import pandas as pd
import wordCutter as wc
import pinyinGenerator as pg
import preTrainingModelApp as ptma

# 数据预处理


def preProcessing(sentences):
    conf.logger.info('dataPreProcessing')
    # 分词
    conf.logger.info("wordCutting")
    wordsList = wc.wordCutting(sentences)
    conf.logger.info("wordCutting end")
    # 规约
    conf.logger.info("Regularing")
    wordsList = wc.regularing(wordsList)
    conf.logger.info("Regularing end")
    if conf.pinyinEmbed:
        # 拼音嵌入
        conf.logger.info("listPinyinEmbedding")
        wordsList = pg.listPinyinEmbedding(wordsList)
        conf.logger.info("listPinyinEmbedding end")
    # 向量化
    conf.logger.info("listEncode")
    model = ptma.read()
    wordsList = ptma.listEncode(model, wordsList)
    conf.logger.info("listEncode end")
    conf.logger.info('dataPreProcessing end')
    # 整理
    X = wordsList
    return X
