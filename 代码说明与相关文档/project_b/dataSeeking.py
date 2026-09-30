import wordCutter as wc
from datetime import datetime
import numpy as np
import pandas as pd
import conf
#数据预览

#绘图查看文本长度分布
def dataDistribute(poswords,negwords):
    #文本长度列表
    lengths=[]
    for words in poswords:
        length=len(words)
        lengths.append(length)
    for words in negwords:
        length=len(words)
        lengths.append(length)
    #计算百分位数
    sortedLen = sorted(lengths)
    percentiles = []
    for i in range(1, 101):
        p = np.percentile(sortedLen, i)
        percentiles.append(p)
    #整理百分位数
    pdict={"p":[i+1 for i in range(100)],"length":percentiles}
    pdf=pd.DataFrame(pdict)
    return pdf

#总体流程
def seeking():
    #分词
    conf.logger.info("wordCutting")
    poswords, negwords = wc.wordCutting(conf.pospath, conf.negpath)
    conf.logger.info("wordCutting end")
    #查看百分位数
    conf.logger.info("dataDistribute")
    pdf=dataDistribute(poswords,negwords)
    conf.logger.info("dataDistribute end")
    conf.logger.info("res")
    pd.set_option('display.max_rows', 100)
    pdfstr='\n'+str(pdf)
    conf.logger.info(pdfstr)