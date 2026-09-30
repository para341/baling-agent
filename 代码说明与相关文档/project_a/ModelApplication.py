import re
import sentenceLevel
import sentenceLevelMod
import conf
import os
import shutil
import shieldWords
import numpy as np
from snownlpModified.sentiment import Sentiment

# 模型应用

#初始化 加载Bayes模型
classifiers = []
for i in range(len(conf.modelpaths)):
    classifier = Sentiment()
    classifier.load(fname=conf.modelpaths[i])
    classifiers.append(classifier)
NB = Sentiment()
NB.load(fname=conf.modelpath)


# 拼音情感词典评估语言情感分数
def ModelAnalysis(sentence):
    ls = re.sub('\\W*', '', sentence)
    sentimentScore = sentenceLevel.sentiment_score(ls)
    return sentimentScore


#情感词典结合NB评估情感分值
def ModelAnalysisCombinedBayes(sentence):
    sentimentScore = sentenceLevelMod.sentiment_score(sentence)
    return sentimentScore

#情感词典结合NB评估情感分值(基于距离阈值)
def ModelAnalysisCombinedBayesByVectorDis(sentence):
    sentimentScore = sentenceLevelMod.sentimentScoreByVectorDis(sentence)
    return sentimentScore

# 拼音情感词典结合bagging评估语言情感分数
def ModelAnalysisViaBagging(sentence):
    #使用词典分析法分析得到情感分值
    ls = re.sub('\\W*', '', sentence)
    sentimentScore = sentenceLevel.sentiment_score(ls)
    #使用sigmoid函数将情感分值转化为期望概率值
    probOfDict = 1 / (1 + np.exp(-sentimentScore))
    #使用Bayes模型分析得到概率值
    global classifiers
    probs = []
    for i in range(len(conf.modelpaths)):
        probs.append(classifiers[i].classify(sentence))
    #加权得到期望概率值
    resProb = probOfDict * conf.weights[0] + probs[0] * conf.weights[
        1] + probs[1] * conf.weights[2] + probs[2] * conf.weights[3] + probs[
            3] * conf.weights[4] + probs[4] * conf.weights[5]
    #转化为(-0.5,0.5)上情感分值并返回
    return resProb - 0.5

#只通过NB评估语言情感倾向
def ModelAnalysisOnlyNB(sentence):
    global NB
    return NB.classify(sentence)
