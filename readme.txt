
          网络欺凌智能检测与防护系统V2.0

一、项目概述
-----------
本项目是一个基于深度学习的网络欺凌智能检测与防护系统V2.0，主要用于检测和分析网络欺凌行为。
系统集成了情感分析、敏感词检测、霸凌分级等功能，支持B站弹幕的实时监测。

二、项目结构
-----------
netbattle/
├── cold/                    # 霸凌检测模型目录
│   ├── config.json          # 模型配置文件
│   ├── pytorch_model.bin    # 预训练模型权重
│   ├── vocab.txt            # 词汇表
│   └── README.md            # 模型说明
│
└── 代码说明与相关文档/      # 核心代码目录
    ├── project_a/           # 主API服务项目
    │   ├── mainAPI.py       # Flask API主入口
    │   ├── coldModel.py     # CoLD/TinyBERT霸凌检测模型
    │   ├── ModelApplication.py    # 情感分析模型
    │   ├── CompareAnalysis.py     # 对比分析模块
    │   ├── shieldWords.py   # 敏感词过滤
    │   ├── generateVectorData.py  # 向量数据生成
    │   ├── conf.py          # 配置文件
    │   ├── requirements.txt # 依赖列表
    │   ├── Data/            # 数据文件目录
    │   ├── models/          # 本地模型文件
    │   ├── logs/            # 日志目录
    │   ├── snownlpModified/ # 中文分词库(修改版)
    │   └── bilibili-dashboard/ # 前端仪表盘
    │
    ├── project_b/           # 数据预处理项目
    │   ├── dataPreProcessing.py   # 数据预处理
    │   ├── preTrainingModelApp.py # 预训练模型应用
    │   └── Data/            # 训练数据
    │
    └── project_c/           # 模型评估项目
        ├── evaluate.ipynb   # 模型评估脚本
        ├── test.ipynb       # 测试脚本
        └── Data/results/    # 评估结果

三、核心功能
-----------
1. 霸凌分级检测 (COLD模型)
   - 支持4级网络欺凌评估：高危、重度、中度、轻度
   - 基于TinyBERT/CoLD深度学习模型
   - 自动降级机制，模型失败时使用传统算法

2. 情感分析
   - 基于朴素贝叶斯的情感分类
   - 支持中文文本情感评分

3. 敏感词过滤
   - 多维度敏感词检测
   - 支持自定义敏感词库

4. 实时数据采集
   - B站弹幕实时爬取
   - 多房间隔离机制

四、运行方式
-----------
1. 安装依赖
   cd 代码说明与相关文档/project_a
   pip install -r requirements.txt

2. 启动服务
   python mainAPI.py

3. 访问API
   - 首页: http://localhost:端口
   - 弹幕采集: /getBulletScreen?roomid=房间号
   - 情感分析: /CommentAnalysis?sentence=文本

五、技术栈
-----------
- Python 3.x
- Flask (API框架)
- PyTorch (深度学习)
- Transformers (HuggingFace)
- SnowNLP (中文NLP)
- Flask-CORS (跨域支持)

六、模型说明
-----------
cold/目录存放霸凌检测模型文件，系统启动时自动加载。
模型支持TinyBERT和CoLD两种架构，自动检测并使用可用模型。
