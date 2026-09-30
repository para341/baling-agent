import numpy as np
from infoLogger import Logger
# 相关配置
# 停用词表
stopwordpath = './Data/stop_words_为准.txt'
# 预训练模型文件目录
mparent = './model/ptm'
# 预训练模型路径
ptmpath = './model/ptm/ptm.bin'
# 预训练模型文件目录(无拼音嵌入)
EXPYmparent = './model/EXPYptm'
# 预训练模型路径(无拼音嵌入)
EXPYptmpath = './model/EXPYptm/expyptm.bin'
# RNN080模型路径
rnnModelPath = './model/rnn080/rnn080.ckpt'
# CNN080模型路径
cnn080ModelPath = './model/cnn080.h5'
# CNNCommon模型路径
cnnCommonModelPath = './model/cnnCommon.h5'
# RNNCommon模型路径
rnnCommonModelPath = './model/rnnCommon/rnnCommon.ckpt'
# 分词数量阈值
wordCountThreshold = 45
# 向量长度
vectorSize = 50
# 拼音向量表
pinyinDict = {
    'c': np.array([0, 0]),
    'ch': np.array([0, 1]),
    's': np.array([0, 2]),
    'sh': np.array([0, 3]),
    'x': np.array([0, 4]),
    'z': np.array([0, 5]),
    'zh': np.array([0, 6]),
    'j': np.array([0, 7]),
    'n': np.array([0, 8]),
    'l': np.array([0, 9]),
    'r': np.array([1, 0]),
    'y': np.array([1, 1]),
    'h': np.array([1, 2]),
    'f': np.array([1, 3]),
    't': np.array([1, 4]),
    'd': np.array([1, 5]),
    'k': np.array([1, 6]),
    'g': np.array([1, 7]),
    'b': np.array([1, 8]),
    'p': np.array([1, 9]),
    'm': np.array([2, 0]),
    'q': np.array([2, 1]),
    'w': np.array([2, 2]),
    'a': np.array([2, 3]),
    'an': np.array([2, 4]),
    'ang': np.array([2, 5]),
    'e': np.array([2, 6]),
    'er': np.array([2, 7]),
    'uo': np.array([2, 8]),
    'ia': np.array([2, 9]),
    'ian': np.array([3, 0]),
    'iang': np.array([3, 1]),
    'i': np.array([3, 2]),
    'ei': np.array([3, 3]),
    'in': np.array([3, 4]),
    'ing': np.array([3, 5]),
    'ie': np.array([3, 6]),
    'ua': np.array([3, 7]),
    'uan': np.array([3, 8]),
    'uang': np.array([3, 9]),
    'ue': np.array([4, 0]),
    've': np.array([4, 1]),
    'en': np.array([4, 2]),
    'eng': np.array([4, 3]),
    'un': np.array([4, 4]),
    'ong': np.array([4, 5]),
    'iong': np.array([4, 6]),
    'u': np.array([4, 7]),
    'v': np.array([4, 8]),
    'iu': np.array([4, 9]),
    'o': np.array([5, 0]),
    'ao': np.array([5, 1]),
    'ou': np.array([5, 2]),
    'ai': np.array([5, 3]),
    'ui': np.array([5, 4]),
    'uai': np.array([5, 5]),
    'iao': np.array([5, 6]),
    '': np.array([9, 9])
}
# 日志模式 1表示生成日志文件 0表示不生成
logmode = 1
# 日志类
logger = Logger(mode=logmode)
# 数据预处理时是否进行拼音嵌入(CNN(RNN)COMMON->False)
pinyinEmbed = False
# 模型选择 0->RNN080 1->CNNCOMMON 2-> CNN080 3->RNNCOMMON
modelSelection = 1
