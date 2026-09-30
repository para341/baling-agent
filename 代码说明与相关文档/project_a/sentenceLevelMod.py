import AiApplication
import codecs
import pickle
from collections import defaultdict
import generateVectorData as gvec
import time  # 在此导入time库，并在开头设置开始时间
import os
import re
import jieba
import conf
import pandas as np

jieba.load_userdict(conf.jiebadictpath)

# 初始化 读取相关数据
# 生成stopword表，需要去除一些否定词和程度词汇
stopwords = set()
with open(conf.basePosPath.replace('pos.txt', 'stop_words_为准.txt'), 'r', encoding='utf-8') as f:
    for word in f:
        stopwords.add(
            word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
# 读取否定词文件
not_word_list = []
with open(conf.basePosPath.replace('pos.txt', '否定词.txt'), 'r+', encoding='utf-8') as f:
    ls = f.readlines()
    not_word_list = [w.strip() for w in ls]
# 读取程度副词文件
degree_dict = defaultdict()
with open(conf.basePosPath.replace('pos.txt', '程度副词.txt'), 'r+', encoding='utf-8') as f:
    degree_list = f.readlines()
    for i in degree_list:
        degree_dict[i.split(',')[0]] = i.split(',')[1]
# 生成新的停用词文件
with open(conf.basePosPath.replace('pos.txt', 'stopwords.txt'), 'w', encoding='utf-8') as f:
    for word in stopwords:
        if (word not in not_word_list) and (word not in degree_dict.keys()):
            f.write(word + '\n')
# 生成新的停用词表
stopwordsNew = set()
with open(conf.basePosPath.replace('pos.txt', 'stopwords.txt'), 'r', encoding='utf-8') as fr:
    for i in fr:
        stopwordsNew.add(i.strip())
# 原始字典
pos_word_dict = dict()
neg_word_dict = dict()
with open(conf.basePosPath.replace('pos.txt', 'BosonNLP_sentiment_score.txt'), 'r', encoding='utf-8') as f:
    for line in f.readlines():
        splits = line.split()
        if (len(splits)) == 0:
            continue
        if float(splits[1]) > 0:
            pos_word_dict[splits[0]] = float(splits[1])
        else:
            neg_word_dict[splits[0]] = float(splits[1])
# 拼音向量字典
pos_pinyin_dict = dict()
neg_pinyin_dict = dict()
with open(conf.basePosPath.replace('pos.txt', 'pos_new_list.pkl'), 'rb') as f:
    for pos in pickle.load(f):
        if len(pos) == 0:
            continue
        pos_pinyin_dict[pos] = 1.0
with open(conf.basePosPath.replace('pos.txt', 'neg_new_list.pkl'), 'rb') as f:
    for neg in pickle.load(f):
        if len(neg) == 0:
            continue
        neg_pinyin_dict[neg] = -1.0


# jieba分词后去除停用词
def seg_word(sentence):
    global stopwordsNew
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    # print(seg_result)
    # print("分词结果：{}".format(list(filter(lambda x: x not in stopwords, seg_result))))
    return list(filter(lambda x: x not in stopwordsNew, seg_result))


# 生成情感词对应字典 记录下标及情感分值
def gen_sen_wordlist(word_list):
    # 引入词库
    global pos_word_dict
    global neg_word_dict
    global pos_pinyin_dict
    global neg_pinyin_dict
    global not_word_list
    global degree_dict
    sen_word = dict()
    # 遍历分词得到的列表
    for i in range(len(word_list)):
        word = word_list[i]
        wordVector = ''
        # 生成纯中文词对应拼音向量
        if gvec.check_only_chinese(word):
            wordVector = gvec.unicode_vec(gvec.generate_vector(word))
        # 找出分词结果中在情感字典中的词(只处理不能转化为拼音向量的词)
        if (word in pos_word_dict.keys() or word in neg_word_dict.keys()
                ) and word not in not_word_list and word not in degree_dict.keys():
            try:
                sen_word[i] = neg_word_dict[word]
            except:
                sen_word[i] = pos_word_dict[word]
        # 找出分词结果中在情感词典中的词(只处理拼音向量)
        elif (
            wordVector in pos_pinyin_dict.keys()
                or wordVector in neg_pinyin_dict.keys()
        ) and word not in not_word_list and word not in degree_dict.keys():
            try:
                sen_word[i] = neg_pinyin_dict[wordVector]
            except:
                sen_word[i] = pos_pinyin_dict[wordVector]
        # 返回情感词下标及其情感分值
    return sen_word

# 生成情感词对应字典 记录下标及情感分值(采用距离阈值算法)
def genSenWordlistByVectorDis(word_list):
    # 引入词库
    global pos_word_dict
    global neg_word_dict
    global pos_pinyin_dict
    global neg_pinyin_dict
    global not_word_list
    global degree_dict
    sen_word = dict()
    # 遍历分词得到的列表
    for i in range(len(word_list)):
        word = word_list[i]
        wordVector = ''
        # 生成纯中文词对应拼音向量
        if gvec.check_only_chinese(word):
            wordVector = gvec.unicode_vec(gvec.generate_vector(word))
        # 找出分词结果中在情感字典中的词(只处理不能转化为拼音向量的词)
        if (word in pos_word_dict.keys() or word in neg_word_dict.keys()
                ) and word not in not_word_list and word not in degree_dict.keys():
            try:
                sen_word[i] = neg_word_dict[word]
            except:
                sen_word[i] = pos_word_dict[word]
        # 找出分词结果中在情感词典中的词(只处理拼音向量)
        elif (
                gvec.vectorInDict(wordVector,pos_pinyin_dict.keys())
                or gvec.vectorInDict(wordVector,neg_pinyin_dict.keys())
        ) and word not in not_word_list and word not in degree_dict.keys():
            fvec1,dis1=gvec.findFamiliar(wordVector,pos_pinyin_dict.keys())
            fvec2,dis2=gvec.findFamiliar(wordVector,neg_pinyin_dict.keys())
            if dis1<dis2:
                sen_word[i] = pos_pinyin_dict[fvec1]
            elif dis1>=dis2:
                sen_word[i] = neg_pinyin_dict[fvec2]
        # 返回情感词下标及其情感分值
    return sen_word


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
    # 引入 否定词 程度副词对应词库
    global not_word_list
    global degree_dict

    # 创建否定词 程度副词 情感词对应字典 记录下标及情感分值
    not_word = dict()
    degree_word = dict()
    sen_word = gen_sen_wordlist(word_list)
    # 分类
    for i in range(len(word_list)):
        word = word_list[i]
        if word in not_word_list and word not in degree_dict.keys():
            # 分词结果中在否定词列表中的词
            not_word[i] = -1
        elif word in degree_dict.keys():
            # 分词结果中在程度副词中的词
            degree_word[i] = degree_dict[word]
    # 返回分类结果
    return sen_word, not_word, degree_word

# 找出文本中的情感词、否定词和程度副词(基于距离阈值算法)
def classifyWordsByVectorDis(word_list):
    # 引入 否定词 程度副词对应词库
    global not_word_list
    global degree_dict

    # 创建否定词 程度副词 情感词对应字典 记录下标及情感分值
    not_word = dict()
    degree_word = dict()
    sen_word = genSenWordlistByVectorDis(word_list)
    # 分类
    for i in range(len(word_list)):
        word = word_list[i]
        if word in not_word_list and word not in degree_dict.keys():
            # 分词结果中在否定词列表中的词
            not_word[i] = -1
        elif word in degree_dict.keys():
            # 分词结果中在程度副词中的词
            degree_word[i] = degree_dict[word]
    # 返回分类结果
    return sen_word, not_word, degree_word


# 计算情感词的分数
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    # 情感分值
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    # 权重初始化为1
    W = 1

    # 处理第1个情感词之前出现的程度副词与否定词
    if len(sentiment_index_list) != 0:
        for j in range(0, sentiment_index_list[0]):
            # 更新权重，如果有否定词，权重取反
            if j in not_word.keys():
                W *= -1
            elif j in degree_word.keys():
                W *= float(degree_word[j])

    # 遍历分词结果
    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            # 权重*情感词得分
            score += W * float(sen_word[i])
            # 情感词下标加一，获取下一个情感词的位置
            sentiment_index += 1
            # 权重重置为1
            W = 1
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in range(sentiment_index_list[sentiment_index],
                               sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，权重取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        W *= float(degree_word[j])
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


# 计算得分
def sentiment_score(sentence):
    # 1.对文档分词
    seg_list = seg_word(sentence)
    # print(seg_list)
    # 2.将分词结果转换成字典，找出情感词、否定词和程度副词
    sen_word, not_word, degree_word = classify_words(seg_list)
    # print("before")
    # print(sen_word)
    # print(not_word)
    # print(degree_word)
    # 3.结合贝叶斯决策论矫正情感分值
    sen_word1, not_word1, degree_word1 = AiApplication.bayesAnalysis(
        seg_list, sen_word, not_word, degree_word)
    # print("after")
    # print(sen_word1)
    # print(not_word1)
    # print(degree_word1)
    # 4.计算得分
    score = score_sentiment(sen_word1, not_word1, degree_word1, seg_list)
    return score

# 计算得分(基于距离阈值)
def sentimentScoreByVectorDis(sentence):
    # 1.对文档分词
    seg_list = seg_word(sentence)
    # print(seg_list)
    # 2.将分词结果转换成字典，找出情感词、否定词和程度副词
    sen_word, not_word, degree_word = classifyWordsByVectorDis(seg_list)
    # print("before")
    # print(sen_word)
    # print(not_word)
    # print(degree_word)
    # 3.结合贝叶斯决策论矫正情感分值
    sen_word1, not_word1, degree_word1 = AiApplication.bayesAnalysis(
        seg_list, sen_word, not_word, degree_word)
    # print("after")
    # print(sen_word1)
    # print(not_word1)
    # print(degree_word1)
    # 4.计算得分
    score = score_sentiment(sen_word1, not_word1, degree_word1, seg_list)
    return score
