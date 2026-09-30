import os
from infoLogger import Logger
import numpy as np

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 相关配置
# 爬虫请求头 (添加了 Origin 提高请求成功率)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://live.bilibili.com/",
    "Origin": "https://live.bilibili.com"
}

# 爬虫请求URL (更改为最新的可用获取弹幕接口)
url = "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory"

# 爬虫请求体数据 (新接口通常只需 GET 请求带 roomid，为兼容原代码结构保留字典)
rqdata = {"roomid": ""}
# 日志模式 1表示生成日志文件 0表示不生成
logmode = 1
# 日志类
logger = Logger(mode=logmode)
# 基础语料路径
basePosPath = os.path.join(BASE_DIR, 'Data', 'pos.txt')
baseNegPath = os.path.join(BASE_DIR, 'Data', 'neg.txt')
# 模型训练成果
# snownlp模型文件所在目录
modelpath = os.path.join(BASE_DIR, 'models', 'sentiment.marshal')
# 自行生成模型文件路径
modelpaths = [
    os.path.join(BASE_DIR, 'models', 'model0'),
    os.path.join(BASE_DIR, 'models', 'model1'),
    os.path.join(BASE_DIR, 'models', 'model2'),
    os.path.join(BASE_DIR, 'models', 'model3'),
    os.path.join(BASE_DIR, 'models', 'model4')
]
# jieba自定义词库路径
jiebadictpath = os.path.join(BASE_DIR, 'Data', 'jiebadict.txt')
#
# 结果权值
weights = [0.3, 0.14, 0.14, 0.14, 0.14, 0.14]
# mongodb url
dburl = 'mongodb://127.0.0.1:27017'
# 爬虫延迟 单位秒
delay = 5
# 词云图背景目录
maskpath = os.path.join(BASE_DIR, 'img', 'heart.png')
# 词云图目标父目录
parentTargetPath = '/opt/module/apache-tomcat-8.5.78/webapps/imgServer/'
# 词云图资源父目录
parentResourcePath = '43.138.22.128:8081/imgServer/'
# 词云图字体目录
ttfpath = os.path.join(BASE_DIR, 'fonts', 'ft.ttf')
# 端口号
port = 8080
# tokenId
tokenId = 'Houduan!'
# 拼音向量表
pinyinDict = {'c': np.array([0, 0]), 'ch': np.array([0, 1]), 's': np.array([0, 2]), 'sh': np.array([0, 3]),
              'x': np.array([0, 4]), 'z': np.array([0, 5]), 'zh': np.array([0, 6]), 'j': np.array([0, 7]), 'n': np.array([0, 8]),
              'l': np.array([0, 9]), 'r': np.array([1, 0]), 'y': np.array([1, 1]), 'h': np.array([1, 2]), 'f': np.array([1, 3]),
              't': np.array([1, 4]), 'd': np.array([1, 5]), 'k': np.array([1, 6]), 'g': np.array([1, 7]), 'b': np.array([1, 8]),
              'p': np.array([1, 9]), 'm': np.array([2, 0]), 'q': np.array([2, 1]), 'w': np.array([2, 2]), 'a': np.array([2, 3]),
              'an': np.array([2, 4]), 'ang': np.array([2, 5]), 'e': np.array([2, 6]), 'er': np.array([2, 7]), 'uo': np.array([2, 8]),
              'ia': np.array([2, 9]), 'ian': np.array([3, 0]), 'iang': np.array([3, 1]), 'i': np.array([3, 2]), 'ei': np.array([3, 3]),
              'in': np.array([3, 4]), 'ing': np.array([3, 5]), 'ie': np.array([3, 6]), 'ua': np.array([3, 7]), 'uan': np.array([3, 8]),
              'uang': np.array([3, 9]), 'ue': np.array([4, 0]), 've': np.array([4, 1]), 'en': np.array([4, 2]), 'eng': np.array([4, 3]),
              'un': np.array([4, 4]), 'ong': np.array([4, 5]), 'iong': np.array([4, 6]), 'u': np.array([4, 7]), 'v': np.array([4, 8]),
              'iu': np.array([4, 9]), 'o': np.array([5, 0]), 'ao': np.array([5, 1]), 'ou': np.array([5, 2]), 'ai': np.array([5, 3]), 'ui': np.array([5, 4]),
              'uai': np.array([5, 5]), 'iao': np.array([5, 6])}
# 阈值
threshold = 1
