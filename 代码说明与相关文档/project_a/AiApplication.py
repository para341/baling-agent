from snownlpModified.sentiment import Sentiment as Classifier
import conf


#机器学习模型应用
# snownlp判断指定词汇为积极词概率
def wordPosProb(word):
    classifier = Classifier()
    classifier.load(fname=conf.modelpath)
    return classifier.classify(word)


#通过贝叶斯决策论对情感分值进行矫正
def bayesAnalysis(word_list, sen_word, not_word, degree_word):
    #对于已知情感词 综合考虑其情感分值
    for i in range(len(word_list)):
        if i in sen_word.keys():
            #对于消极词汇 考虑其为消极词的概率
            if sen_word[i] < 0:
                sen_word[i] *= 1 - wordPosProb(word_list[i])
            #对于积极词汇 考虑其为积极词的概率
            if sen_word[i] > 0:
                sen_word[i] *= wordPosProb(word_list[i])
    #对于非否定词 非程度副词及非情感词典中词 通过AI给出其情感分值
    for i in range(len(word_list)):
        if i not in sen_word.keys() and i not in not_word.keys(
        ) and i not in degree_word.keys():
            word = word_list[i]
            sen_word[i] = wordPosProb(word) - 0.5
    return sen_word, not_word, degree_word