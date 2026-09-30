import sys
import os
import logging
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

COLD_AVAILABLE = False
bully_model = None
bully_tokenizer = None

def load_model():
    """
    加载霸凌检测模型（支持 CoLD、TinyBERT 等）
    """
    global COLD_AVAILABLE, bully_model, bully_tokenizer
    
    try:
        from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
        import json
        
        # 尝试加载 TinyBERT（新模型）
        tinybert_path = "D:\\netbattle\\cold"
        # 尝试加载 CoLD（原模型，如果存在）
        cold_path = "D:\\netbattle\\cold"
        
        model_path = None
        model_type = None
        
        if os.path.exists(tinybert_path):
            model_path = tinybert_path
            model_type = "tinybert"
            logger.info(f"找到 TinyBERT 模型: {model_path}")
        elif os.path.exists(cold_path):
            model_path = cold_path
            model_type = "cold"
            logger.info(f"找到 CoLD 模型: {model_path}")
        else:
            logger.warning("未找到任何模型")
            return False
        
        # 加载 tokenizer 和模型
        logger.info("正在加载模型...")
        
        # 加载配置文件
        with open(os.path.join(model_path, "config.json"), "r", encoding="utf-8") as f:
            config_dict = json.load(f)
        
        # 创建 BertConfig
        config = BertConfig(
            vocab_size=config_dict.get("vocab_size", 21128),
            hidden_size=config_dict.get("hidden_size", 256),
            num_hidden_layers=config_dict.get("num_hidden_layers", 4),
            num_attention_heads=config_dict.get("num_attention_heads", 4),
            intermediate_size=config_dict.get("intermediate_size", 1024),
            hidden_act=config_dict.get("hidden_act", "gelu"),
            hidden_dropout_prob=config_dict.get("hidden_dropout_prob", 0.1),
            attention_probs_dropout_prob=config_dict.get("attention_probs_dropout_prob", 0.1),
            max_position_embeddings=config_dict.get("max_position_embeddings", 512),
            type_vocab_size=config_dict.get("type_vocab_size", 2),
            layer_norm_eps=config_dict.get("layer_norm_eps", 1e-12),
            num_labels=2
        )
        
        # 创建模型
        bully_model = BertForSequenceClassification(config)
        
        # 加载权重
        state_dict = torch.load(os.path.join(model_path, "pytorch_model.bin"), map_location="cpu", weights_only=False)
        
        # 权重映射: encoder -> bert
        new_state_dict = {}
        for key, value in state_dict.items():
            new_key = key
            if key.startswith("encoder."):
                if key.startswith("encoder.embeddings"):
                    new_key = key.replace("encoder.embeddings.", "bert.embeddings.")
                elif key.startswith("encoder.encoder.layer"):
                    new_key = key.replace("encoder.encoder.layer.", "bert.encoder.layer.")
                elif key.startswith("encoder.pooler"):
                    new_key = key.replace("encoder.pooler.", "bert.pooler.")
            new_state_dict[new_key] = value
        
        # 加载到模型
        bully_model.load_state_dict(new_state_dict, strict=False)
        bully_model.eval()
        
        # 加载 tokenizer
        bully_tokenizer = BertTokenizer(os.path.join(model_path, "vocab.txt"))
        
        COLD_AVAILABLE = True
        logger.info(f"{model_type.upper()} 模型加载成功！")
        return True
        
    except Exception as e:
        logger.warning(f"模型加载失败: {e}")
        import traceback
        logger.warning(traceback.format_exc())
        logger.warning("将使用原有算法作为降级方案")
        return False

# 初始化加载
load_model()


def calculate_bully_level_v2(text):
    """
    霸凌分级函数（使用深度学习模型）
    """
    if not COLD_AVAILABLE or not bully_model or not bully_tokenizer:
        return None
    
    try:
        inputs = bully_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = bully_model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
            # 获取负面/霸凌概率
            # TinyBERT: label 0=负面, 1=正面
            # CoLD: label 0=正常, 1=攻击性
            negative_prob = probabilities[0][0].item()  # 负面概率
            
            # 转换为霸凌等级（负面概率越高，霸凌等级越高）
            offensive_score = negative_prob
        
        if offensive_score > 0.7:
            return {
                "level": 4,
                "levelName": "高危",
                "action": "拦截 + 预警上报",
                "color": "#f87171",
                "score": round(offensive_score, 3),
                "method": "TinyBERT"
            }
        elif offensive_score > 0.5:
            return {
                "level": 3,
                "levelName": "重度",
                "action": "警告并折叠",
                "color": "#fb923c",
                "score": round(offensive_score, 3),
                "method": "TinyBERT"
            }
        elif offensive_score > 0.3:
            return {
                "level": 2,
                "levelName": "中度",
                "action": "警告提示",
                "color": "#fbbf24",
                "score": round(offensive_score, 3),
                "method": "TinyBERT"
            }
        elif offensive_score > 0.1:
            return {
                "level": 1,
                "levelName": "轻度",
                "action": "善意提醒",
                "color": "#60a5fa",
                "score": round(offensive_score, 3),
                "method": "TinyBERT"
            }
        else:
            return {
                "level": 0,
                "levelName": "常规",
                "action": "正常放行",
                "color": "#34d399",
                "score": round(offensive_score, 3),
                "method": "TinyBERT"
            }
    except Exception as e:
        logger.error(f"模型分析出错: {e}")
        return None


def get_model_status():
    """
    获取模型状态信息
    """
    tinybert_path = "D:\\netbattle\\cold"
    cold_path = "D:\\netbattle\\cold"
    
    status = {
        "available": COLD_AVAILABLE,
        "tinybert_exists": os.path.exists(tinybert_path),
        "cold_exists": os.path.exists(cold_path),
        "current_model": "TinyBERT" if os.path.exists(tinybert_path) else ("CoLD" if os.path.exists(cold_path) else "None")
    }
    
    return status


if __name__ == "__main__":
    # 测试
    print("=" * 60)
    print("霸凌检测模型测试")
    print("=" * 60)
    
    status = get_model_status()
    print(f"\n模型状态: {status}")
    
    if COLD_AVAILABLE:
        test_texts = [
            "你真是个废物，没人喜欢你",
            "今天天气真好，心情不错",
            "你怎么这么笨，这么简单都不会",
            "这首歌真好听，爱了爱了",
            "滚出去，这里不欢迎你"
        ]
        
        print("\n测试样例:")
        for text in test_texts:
            result = calculate_bully_level_v2(text)
            print(f"\n文本: {text}")
            print(f"结果: {result}")
    else:
        print("模型未加载，无法测试")
