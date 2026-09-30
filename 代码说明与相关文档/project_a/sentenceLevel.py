import pickle
from collections import defaultdict
import generateVectorData as gv
import time  # 在此导入time库，并在开头设置开始时间
import os
import re
import conf
import jieba

jieba.load_userdict(conf.jiebadictpath)
import codecs

# 生成stopword表，需要去除一些否定词和程度词汇
stopwords = set()
fr = open(conf.basePosPath.replace('pos.txt', 'stop_words_为准.txt'), 'r', encoding='utf-8')
for word in fr:
    stopwords.add(
        word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
# 读取否定词文件
not_word_file = open(conf.basePosPath.replace('pos.txt', '否定词.txt'), 'r+', encoding='utf-8')
not_word_list = not_word_file.readlines()
not_word_list = [w.strip() for w in not_word_list]

# 读取程度副词文件
degree_file = open(conf.basePosPath.replace('pos.txt', '程度副词.txt'), 'r+', encoding='utf-8')
degree_list = degree_file.readlines()
degree_list = [item.split(',')[0] for item in degree_list]
# print(degree_list)

# 生成新的停用词表
with open(conf.basePosPath.replace('pos.txt', 'stopwords.txt'), 'w', encoding='utf-8') as f:
    for word in stopwords:
        if (word not in not_word_list) and (word not in degree_list):
            f.write(word + '\n')

# 读数据
# 原始字典
f1 = open(conf.basePosPath.replace('pos.txt', 'neg_word_list.pkl'), 'rb')
neg_word_list = pickle.load(f1)
f2 = open(conf.basePosPath.replace('pos.txt', 'pos_word_list.pkl'), 'rb')
pos_word_list = pickle.load(f2)

# 拼音向量后的压缩字典
f3 = open(conf.basePosPath.replace('pos.txt', 'neg_new_list.pkl'), 'rb')
neg_new_list = pickle.load(f3)
f4 = open(conf.basePosPath.replace('pos.txt', 'pos_new_list.pkl'), 'rb')
pos_new_list = pickle.load(f4)

# 拼音向量对应的中文欺凌词
f5 = open(conf.basePosPath.replace('pos.txt', 'neg_vec_chinese.pkl'), 'rb')
neg_vec_chinese = pickle.load(f5)
f6 = open(conf.basePosPath.replace('pos.txt', 'pos_vec_chinese.pkl'), 'rb')
pos_vec_chinese = pickle.load(f6)

#
# print(neg_new_list)
# print(pos_new_list)
# index = 0
# for neg in neg_new_list:
#     for pos in pos_new_list:
#         if neg == pos:
#             #print('存在一样的')
#             index += 1
# print('消极词有{}个，积极词有{}个，其中，一共有{}个向量是一样的。'.format(len(neg_new_list),len(pos_new_list),index))


# jieba分词后去除停用词
def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    # print(seg_result)
    stopwords = set()
    with open('./Data/stopwords.txt', 'r', encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    # print("分词结果：{}".format(list(filter(lambda x: x not in stopwords, seg_result))))
    return list(filter(lambda x: x not in stopwords, seg_result))


# 生成情感词对应字典
def gen_sen_wordlist(pos_sen_dict, neg_sen_dict, not_word_list, degree_dict,
                     word_list):
    sen_word = dict()
    #遍历分词得到的列表
    for i in range(len(word_list)):
        word = word_list[i]
        #生成纯中文词对应拼音向量
        if '\u4e00' <= word <= '\u9fff':
            if gv.check_only_chinese(word):
                word_vec = gv.unicode_vec(gv.generate_vector(word))
        # 找出分词结果中在情感字典中的词(只处理不能转化为拼音向量的词)
        if (word in pos_sen_dict.keys() or word in neg_sen_dict.keys()
            ) and word not in not_word_list and word not in degree_dict.keys():
            try:
                sen_word[i] = neg_sen_dict[word]
            except:
                sen_word[i] = pos_sen_dict[word]
        # 找出分词结果中在情感词典中的词(只处理拼音向量)
        elif (word_vec in pos_sen_dict.keys() or word_vec in neg_sen_dict.keys(
        )) and word not in not_word_list and word not in degree_dict.keys():
            try:
                sen_word[i] = neg_sen_dict[word_vec]
            except:
                sen_word[i] = pos_sen_dict[word_vec]
        # 返回情感词下标及其情感分值
    return sen_word


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
    #导入情感词典
    global pos_new_list
    global neg_new_list
    # 创建情感字典
    pos_sen_dict = defaultdict()
    neg_sen_dict = defaultdict()
    # 添加情感分值
    # 添加规则 所有积极词对应拼音向量情感分值为+1 所有消极词对应拼音向量情感分值为-1
    for pos in pos_new_list:
        pos_sen_dict[pos] = 1.0
    for neg in neg_new_list:
        # print(neg)
        neg_sen_dict[neg] = -1.0

    # try:print(neg_sen_dict['毛病'])
    # except:print(pos_sen_dict['毛病'])

    # 读取否定词文件
    not_word_file = open('./Data/否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    not_word_list = [w.strip() for w in not_word_list]

    # print("==========================================================================")
    # 读取程度副词文件
    degree_file = open('./Data/程度副词.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_dict = defaultdict()
    for i in degree_list:
        degree_dict[i.split(',')[0]] = i.split(',')[1]
    # print(degree_dict)

    #否定词 程度副词 情感词对应字典 记录下标及情感分值
    not_word = dict()
    degree_word = dict()
    sen_word = gen_sen_wordlist(pos_sen_dict, neg_sen_dict, not_word_list,
                                degree_dict, word_list)

    # 分类
    for i in range(len(word_list)):
        word = word_list[i]
        # print(word)
        if word in not_word_list and word not in degree_dict.keys():
            # 分词结果中在否定词列表中的词
            not_word[i] = -1
        elif word in degree_dict.keys():
            # 分词结果中在程度副词中的词
            degree_word[i] = degree_dict[word]

    # 关闭打开的文件

    not_word_file.close()
    degree_file.close()
    # 返回分类结果
    return sen_word, not_word, degree_word


# 计算情感词的分数
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    # 权重初始化为1
    W = 1
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())

    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            # 权重*情感词得分
            score += W * float(sen_word[i])
            # 情感词下标加一，获取下一个情感词的位置
            sentiment_index += 1
            # print(score)
            # if sentiment_index == 0:
            #     for a_index in range(0,sentiment_index_list[sentiment_index]):
            #         if a_index in not_word.keys():
            #             W *= -1
            #         elif a_index in degree_word.keys():
            #             W *= float(degree_word[a_index])
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
    # print(sen_word)
    # print(not_word)
    # print(degree_word)
    # 3.计算得分
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score


# if __name__ == "__main__":
#
#     start = time.perf_counter()
#
#     sentence_list = ['踏马的，你真的好像有病一样', '你除了扔水里淹不死，其他真的很一无是处', "不错，看来你也没有那么辣鸡", "Fuck，我从未见过有如此厚颜无耻之人","蔚汀"]
#     for sen in sentence_list:
#         print("「"+sen + "」的情感分值为：",sentiment_score(sen))
#
#     end = time.perf_counter()# 在程序运行结束的位置添加结束时间
#     print()
#     print("使用拼音向量化后的词典进行情感倾向分析耗时：{}".format(end - start))
#     # 再将其进行打印，即可显示出程序完成的运行耗时
