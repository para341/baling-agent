import pickle
import pandas as pd
from pypinyin import lazy_pinyin, Style
import numpy as np
from collections import defaultdict
import re
import copy
import conf

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

# 切分为声母和韵母


def cut_pinyin(word):
    shengmu_list = lazy_pinyin(word, style=Style.INITIALS, strict=False)
    yunmu_list = lazy_pinyin(word, style=Style.FINALS, strict=False)

    # 删除生僻字
    for i in range(len(yunmu_list)):
        if yunmu_list[i] not in sum(y_list, []):
            yunmu_list[i] = ''
        else:
            continue

    return shengmu_list, yunmu_list


# 将词库里的词语进行向量化处理
def generate_vector(word):
    test = np.array([],dtype=int)

    # 对含有字母B、数字8、字母x的词语进行转换处理
    if 'B' in word or 'b' in word:
        w_list = list(word)
        w_list[len(w_list) - 1] = '逼'
        word = ''.join(w_list)
    if 'X' in word or 'x' in word:
        w_list = list(word)
        w_list[len(w_list) - 1] = '叉'
        word = ''.join(w_list)
    if '8' in word:
        w_list = list(word)
        w_list[len(w_list) - 1] = '巴'
        word = ''.join(w_list)
    sm_list, ym_list = cut_pinyin(word)
    for index in range(len(sm_list)):
        # 声母韵母都存在
        if sm_list[index] != '' and ym_list[index] != '':
            if sm_list[index] in pinyin_dict and ym_list[index] in pinyin_dict:
                test = np.append(test, pinyin_dict[sm_list[index]])
                test = np.append(test, pinyin_dict[ym_list[index]])
        # 不含声母情况，例如：额、啊
        elif sm_list[index] == '' and ym_list[index] != '':
            if ym_list[index] in pinyin_dict:
                test = np.append(test, pinyin_dict[ym_list[index]])
        elif sm_list[index] != '' and ym_list[index] == '':
            if sm_list[index] in pinyin_dict:
                test = np.append(test, pinyin_dict[sm_list[index]])
        # 两者都为空，跳过
        else:
            continue
    return test


# 检测是否只包含中文
def check_only_chinese(key):
    key_list = list(key)
    for char in key_list:
        if '\u4e00' <= char <= '\u9fff':
            continue
        else:
            return False
    return True


def unicode_vec(word_vec):
    return '.'.join(list(map(str, word_vec.tolist())))

# 拼音向量距离度量


def vectorDis(vecstr1, vecstr2):
    # 处理空字符串情况
    if not vecstr1 or not vecstr2:
        return 2147483647
    
    # 转化为向量
    try:
        vec1 = np.array(vecstr1.split('.'), dtype=float)
    except Exception as e:
        return 2147483647
    
    vec2 = np.array([])
    try:
        vec2 = np.array(vecstr2.split('.'), dtype=float)
    except Exception as e:
        return 2147483647

    # 统一长度
    if vec1.size < vec2.size:
        zeros = np.array([0 for i in range(vec2.size - vec1.size)])
        vec1 = np.append(vec1, zeros)
    if vec1.size > vec2.size:
        zeros = np.array([0 for i in range(vec1.size - vec2.size)])
        vec2 = np.append(vec2, zeros)
    # 计算悖可夫斯基距离 p=2
    distance = np.power(np.power(np.abs(vec1 - vec2), 2).sum(), 1 / 2)
    return distance

# 判断拼音向量是否在keys中


def vectorInDict(vecstr, keys):
    for key in keys:
        # 距离不大于阈值认为相同
        if vectorDis(vecstr, key) <= conf.threshold:
            return True
    return False

# 从keys中找到距离最近的拼音向量


def findFamiliar(vecstr, keys):
    mindis = 2147483647
    fvecstr = ""
    for key in keys:
        # 更新最短距离
        dis = vectorDis(vecstr, key)
        if dis < mindis:
            mindis = dis
            fvecstr = key
    return fvecstr, mindis

    # 构建向量：中文 词库


def ge_vec_chinese_dict(word_list, file_name):
    new_word_list = copy.deepcopy(word_list)
    # 构建坏词编码，坏词向量化
    word_dict = {}
    for i in range(len(word_list)):
        if '\u4e00' <= word_list[i] <= '\u9fff':
            if check_only_chinese(word_list[i]):
                # continue
                word_vector = generate_vector(word_list[i])
                word_dict[word_list[i]] = word_vector
                new_word_list[i] = unicode_vec(word_vector)
                # new_word_list[i] = word_vector
                # num_list[i] = unicode_vec(word_vector)
            elif 'b' in word_list[i] or 'B' in word_list[
                    i] or 'X' in word_list[i] or 'x' in word_list[i]:
                word_vector = generate_vector(word_list[i])
                word_dict[word_list[i]] = word_vector
                new_word_list[i] = unicode_vec(word_vector)
                # new_word_list[i] = word_vector
                # num_list[i] = unicode_vec(word_vector)
            else:
                continue
    '''
    tolist:将array类型的数据转化成整型列表，例如：array(0,1,0,0)→[0,1,0,0]
    list+map:将整型列表转化成字符串，例如：[0,1,0,0]→['0','1','0','0']
    ''.join:将列表转化成字符串，例如：['0','1','0','0']→'0010' 
    '''
    word_key = []
    for num in list(word_dict.values()):
        word_key.append('.'.join(list(map(str, num.tolist()))))
    word_value = list(word_dict.keys())

    # 键值对互换
    dic_new = dict(zip(word_key, word_value))

    # 保存
    vec_chinese_base = open(u"./Data/" + file_name + ".pkl", 'wb')
    pickle.dump(dic_new, vec_chinese_base)
    vec_chinese_base.close()
    # return dic_new,new_word_list,num_list
    return dic_new, new_word_list


if __name__ == "__main__":

    # 读取情感词典文件
    sen_file = open('./Data/BosonNLP_sentiment_score.txt',
                    'r+',
                    encoding='utf-8')
    # 获取词典文件内容
    sen_list = sen_file.readlines()
    # 创建情感字典
    sen_dict = defaultdict()
    # 读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
    for i in sen_list:
        if len(i.split(' ')) == 2:
            sen_dict[i.split(' ')[0]] = i.split(' ')[1]

    neg_word_list = []
    pos_word_list = []
    print('原情感词库一共包含：{}个情感词'.format(len(sen_dict.keys())))
    for key in list(sen_dict.keys()):
        if float(sen_dict[key]) < 0:
            neg_word_list.append(key)
        else:
            pos_word_list.append(key)

    dirty_word = pd.read_table('./Data/dirty_word.txt',
                               encoding='utf-8',
                               header=None)
    for dirty in list(dirty_word[0]):
        neg_word_list.append(dirty)

    # print(len(neg_word_list))

    neg_dic, neg_new_list = ge_vec_chinese_dict(neg_word_list,
                                                'neg_vec_chinese')
    pos_dic, pos_new_list = ge_vec_chinese_dict(pos_word_list,
                                                'pos_vec_chinese')

    print('原消极词库一共有{}个'.format(len(neg_word_list)))
    # print(neg_word_list[:500])
    print('现消极词库一共有{}个'.format(len(set(neg_new_list))))
    print('原积极词库一共有{}个'.format(len(pos_word_list)))
    print('现积极词库一共有{}个'.format(len(set(pos_new_list))))
    new_num = (len(set(neg_new_list))) + (len(set(pos_new_list)))
    print('现情感词库一共包含：{}个情感词'.format(new_num))

    output1 = open(u"./Data/neg_word_list.pkl", 'wb')
    pickle.dump(neg_word_list, output1)  # 索引字典
    output1.close()

    output2 = open(u"./Data/pos_word_list.pkl", 'wb')
    pickle.dump(pos_word_list, output2)  # 索引字典
    output2.close()

    output3 = open(u"./Data/neg_new_list.pkl", 'wb')
    pickle.dump(list(set(neg_new_list)), output3)  # 索引字典
    output3.close()

    output4 = open(u"./Data/pos_new_list.pkl", 'wb')
    pickle.dump(list(set(pos_new_list)), output4)  # 索引字典
    output4.close()
