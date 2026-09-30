import wordCutter as wc
import conf
import dataPreProcessing as dpp
import modelApp as ma
from sklearn import metrics
import pandas as pd
import sys
import numpy as np
from tensorflow.keras.models import load_model

df = pd.read_csv('./Data/data.csv')
sentences = df['sentences'].tolist()
labels = df['labels'].tolist()
wordsList = wc.wordCutting(sentences)
newsentences = []
newlabels = []
for i in range(len(sentences)):
    if (len(wordsList[i]) > conf.wordCountThreshold):
        continue
    newsentences.append(sentences[i])
    newlabels.append(labels[i])

conf.logger.info("modelSelected ? (y/n)")
option=input()
if option != 'y':
    sys.exit()
conf.logger.info("model {}".format(conf.modelSelection))

ma.load()
X = dpp.preProcessing(newsentences)
y = newlabels
ypred = ma.predict(X)
conf.logger.info('\n'+str(metrics.classification_report(y, ypred)))
