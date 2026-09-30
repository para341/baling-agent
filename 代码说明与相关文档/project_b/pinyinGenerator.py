import pickle
import pandas as pd
import pypinyin
from pypinyin import lazy_pinyin, Style, pinyin
import numpy as np
from collections import defaultdict
import re
import copy
import conf

# 拼音生成

# 声母表 24
s_list = [['b'], ['c'], ['d'], ['f'], ['g'], ['h'], ['j'], ['k'], ['l'], ['m'],
          ['n'], ['p'], ['q'], ['r'], ['s'], ['t'], ['w'], ['x'], ['y'], ['z'],
          ['s'], ['zh'], ['ch'], ['sh']]
# 韵母表 34
y_list = [['a'], ['e'], ['i'], ['o'], ['u'], ['v'], ['ai'], ['ui'], ['iu'],
          ['ei'], ['ie'], ['ao'], ['ou'], ['uo'], ['ue'], ['ve'], ['er'],
          ['an'], ['en'], ['in'], ['un'], ['ua'], ['ia'], ['ang'], ['eng'],
          ['ing'], ['ong'], ['ian'], ['iao'], ['uan'], ['uai'], ['iong'],
          ['iang'], ['uang']]

# 向量组, {拼音: 向量}
pinyin_dict = conf.pinyinDict

# 拼音切分


def cutPinyin(word):
    shengmu_list = lazy_pinyin(word, style=Style.INITIALS, strict=False)
    yunmu_list = lazy_pinyin(word, style=Style.FINALS, strict=False)
    # tone_list = lazy_pinyin(word, style=Style.TONE2)

    # 删除生僻字
    for i in range(len(yunmu_list)):
        if yunmu_list[i] not in sum(y_list, []):
            yunmu_list[i] = ''
        else:
            continue

    # return shengmu_list, yunmu_list, tone_list
    return shengmu_list, yunmu_list


# 拼音向量生成
def generatePinyinVector(word):
    test = np.array([], dtype=int)

    # sm_list, ym_list, tone_list = cutPinyin(word)
    sm_list, ym_list = cutPinyin(word)
    # 处理声母 韵母
    for index in range(len(sm_list)):
        # 声母韵母都存在
        if sm_list[index] != '' and ym_list[index] != '':
            test = np.append(test, pinyin_dict[sm_list[index]])
            test = np.append(test, pinyin_dict[ym_list[index]])
        # 不含声母情况，例如：额、啊
        if sm_list[index] == '' and ym_list[index] != '':
            test = np.append(test, pinyin_dict[ym_list[index]])
        if sm_list[index] != '' and ym_list[index] == '':
            test = np.append(test, pinyin_dict[ym_list[index]])
        if sm_list[index] == '' and ym_list[index] == '':
            continue
    # 处理声调
    # for index in range(len(tone_list)):
    #     tonels = re.findall(r'\d+', tone_list[index])
    #     if len(tonels) == 0:
    #         continue
    #     tone = int(tonels[0])
    #     test = np.append(test, tone)
    return test.tolist()

# 拼音嵌入


def pinyinEmbedding(word):
    embedWord = ''
    # 遍历词中每个字符
    for c in word:
        # 跳过非汉字
        if not '\u4e00' <= c <= '\u9fff':
            embedWord = embedWord+c
            continue
        # 生成汉字拼音向量
        vec = generatePinyinVector(c)
        # 添加汉字与对应拼音
        embedWord = embedWord + c
        for i in vec:
            embedWord = embedWord + chr(i)
    return embedWord

# 词列表拼音嵌入


def listPinyinEmbedding(posWords, negWords):
    # 遍历积极语料每个词
    for words in posWords:
        for i in range(len(words)):
            # 嵌入拼音
            words[i] = pinyinEmbedding(words[i])
    # 遍历消极语料中每个词
    for words in negWords:
        for i in range(len(words)):
            # 嵌入拼音
            words[i] = pinyinEmbedding(words[i])
    return posWords, negWords

    # 字向量生成

    # def generateCharVector(word):
    #     unicodels = []
    #     for i in word:
    #         unicodels.append(ord(i) - 0x4e00)
    #     unicodeArr = np.array(unicodels)
    #     return unicodeArr

    # 词向量生成

    # def generateWordVector(word):
    #     unicodeVec = generateCharVector(word)
    #     pinyinVec = generatePinyinVector(word)
    #     wordVec = np.array([], dtype=int)
    #     for i in unicodeVec:
    #         wordVec = np.append(wordVec, i)
    #     for i in pinyinVec:
    #         wordVec = np.append(wordVec, i)
    #     return wordVec

    # 检测是否只包含中文


def checkOnlyChinese(key):
    key_list = list(key)
    for char in key_list:
        if '\u4e00' <= char <= '\u9fff':
            continue
        else:
            return False
    return True
