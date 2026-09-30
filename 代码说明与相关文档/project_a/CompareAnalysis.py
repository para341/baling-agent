from bs4 import BeautifulSoup as bs
import requests as rq
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ModelApplication
import conf
import shieldWords
import re

#初始化 加载基础语料库
poslist = shieldWords.read_txt(conf.basePosPath)
neglist = shieldWords.read_txt(conf.baseNegPath)


# 通过爬虫实现例句生成
def compareAnalysis(text):
    #config
    rq.packages.urllib3.disable_warnings(InsecureRequestWarning)
    #flag
    IsConnectok = True
    #发起请求
    url = 'https://tieba.baidu.com/f/search/res?ie=utf-8&qw={}'.format(text)
    try:
        rs = rq.get(
            url,
            verify=False,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
            })
    except rq.exceptions.ConnectTimeout:
        print("RequestTimeOut!")
        IsConnectok = False
    except rq.exceptions.ReadTimeout:
        print("RequestTimeOut!")
        IsConnectok = False
    except rq.exceptions.ConnectionError:
        print("ConnectFailed!")
        IsConnectok = False
    except:
        IsConnectok = False
    #请求失败
    if IsConnectok == False:
        print("Request Failed")
        return
    #提取例句
    soup = bs(rs.text, 'lxml')
    titles = soup.select('span[class*="p_title"]')
    contents = soup.select('div[class*="p_content"]')
    examples = []
    for i in titles:
        #只提取包含已知文本的例句
        if text in i.get_text():
            examples.append(i.get_text())
    for i in contents:
        if text in i.get_text():
            examples.append(i.get_text())
    #长度判断
    #长度小于3时补充3例句
    if len(examples) < 3:
        for i in range(3):
            examples.append(text)
    #截取前3个例句
    examples = examples[0:3]
    #情感分值
    sentiments = []
    for i in range(3):
        sentiments.append(
            ModelApplication.ModelAnalysisCombinedBayes(examples[i]))
    return examples, sentiments


#通过搜索语料库实现例句生成
def compareAnalysisViaBase(text):
    global poslist
    global neglist
    #寻找例句
    examples = []
    for i in poslist:
        #只提取包含已知文本的例句
        if text in i:
            examples.append(i)
    for i in neglist:
        if text in i:
            examples.append(i)
    #长度判断
    #长度小于3时补充3例句
    if len(examples) < 3:
        for i in range(3):
            examples.append(text)
    #截取前3个例句
    examples = examples[0:3]
    #调整例句长度
    for i in range(3):
        part = ""
        #只取其中包含已知文本部分
        for j in examples[i].split('。'):
            if text in j:
                part = j
                break
        examples[i] = part
    #情感分值
    sentiments = []
    for i in range(3):
        sentiments.append(
            ModelApplication.ModelAnalysisCombinedBayes(examples[i]))
    return examples, sentiments