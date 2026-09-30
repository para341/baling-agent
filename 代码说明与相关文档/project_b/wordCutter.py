from txtReader import read_txt
import jieba
import conf
import os
import sys
import datetime
import pinyinGenerator as pg
# 分词

# 初始化 读取相关数据
# 生成stopword表，需要去除一些否定词和程度词汇
stopwords = set()
with open(conf.stopwordpath, 'r', encoding='utf-8') as f:
    for word in f:
        stopwords.add(
            word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。

# jieba分词后去除停用词


def seg_word(sentence):
    global stopwords
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    return list(filter(lambda x: x not in stopwords, seg_result))


# 读入积极 消极语料 分词 去除停用词

def wordCutting(pospath, negpath):
    # 读入积极 消极语料
    poslines = read_txt(pospath)
    neglines = read_txt(negpath)
    # 转化积极语料成分词列表
    posWords = []
    for line in poslines:
        words = seg_word(line)
        posWords.append(words)
    # 转化消极语料成分词列表
    negWords = []
    for line in neglines:
        words = seg_word(line)
        negWords.append(words)
    # 返回二维分词列表
    return posWords, negWords
   
# 分词结果规约
def regularing(poswords,negwords):
    newPosWords=[]
    newNegWords=[]
    #遍历积极语料
    for line in poswords:
        #去除过长语料
        if len(line)>conf.wordCountThreshold:
            continue
        #扩充较短语料
        if len(line)<conf.wordCountThreshold:
            newPosWords.append(line+['' for i in range(conf.wordCountThreshold-len(line))])
            continue
        #添加长度符合条件语料
        newPosWords.append(line)
    #遍历积极语料
    for line in negwords:
        #去除过长语料
        if len(line)>conf.wordCountThreshold:
            continue
        #扩充较短语料
        if len(line)<conf.wordCountThreshold:
            newNegWords.append(line+['' for i in range(conf.wordCountThreshold-len(line))])
            continue
        #添加长度符合条件语料
        newNegWords.append(line)
    return newPosWords,newNegWords