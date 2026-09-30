"""
阿里云百炼语音识别服务
使用 Paraformer 模型进行语音转文字
免费额度：每月 36,000 秒（10小时）
文档：https://help.aliyun.com/zh/dashscope/developer-reference/paraformer-api-details
"""
import requests
import json
import base64
import os

# 阿里云百炼 API 配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "your-api-key-here")
DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"


class AliyunSpeechService:
    """阿里云语音识别服务"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or DASHSCOPE_API_KEY
        if self.api_key == "your-api-key-here":
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量或在代码中传入 api_key")
    
    def recognize(self, audio_path, model="paraformer-v2"):
        """
        识别语音文件
        
        Args:
            audio_path: 音频文件路径（支持 wav, mp3, pcm 等格式）
            model: 模型名称，默认 paraformer-v2
            
        Returns:
            dict: {
                "success": True/False,
                "text": "识别的文字内容",
                "duration": 音频时长（秒）,
                "error": 错误信息（如果有）
            }
        """
        try:
            # 读取音频文件并转为 base64
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")
            
            # 获取文件格式
            file_ext = os.path.splitext(audio_path)[1].lower().replace(".", "")
            if file_ext not in ["wav", "mp3", "pcm", "m4a", "wma"]:
                file_ext = "wav"  # 默认格式
            
            # 构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "input": {
                    "audio": audio_base64,
                    "audio_format": file_ext
                },
                "parameters": {
                    "language_hints": ["zh", "en"]  # 支持中英文
                }
            }
            
            # 发送请求
            response = requests.post(
                DASHSCOPE_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                if "output" in result and "text" in result["output"]:
                    return {
                        "success": True,
                        "text": result["output"]["text"],
                        "duration": result["output"].get("duration", 0),
                        "error": None
                    }
                else:
                    return {
                        "success": False,
                        "text": "",
                        "duration": 0,
                        "error": "响应格式异常"
                    }
            else:
                return {
                    "success": False,
                    "text": "",
                    "duration": 0,
                    "error": f"API 错误: {response.status_code}, {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "duration": 0,
                "error": str(e)
            }
    
    def recognize_and_analyze(self, audio_path, bully_analyzer):
        """
        识别语音并分析霸凌指数
        
        Args:
            audio_path: 音频文件路径
            bully_analyzer: 霸凌分析函数（如 calculate_bully_level_v2）
            
        Returns:
            dict: 包含识别结果和霸凌分析
        """
        # 1. 语音识别
        recognition_result = self.recognize(audio_path)
        
        if not recognition_result["success"]:
            return {
                "success": False,
                "error": recognition_result["error"],
                "text": "",
                "bully_analysis": None
            }
        
        # 2. 霸凌分析
        text = recognition_result["text"]
        bully_result = bully_analyzer(text)
        
        return {
            "success": True,
            "text": text,
            "duration": recognition_result["duration"],
            "bully_analysis": bully_result,
            "error": None
        }


# 便捷函数
def recognize_speech(audio_path, api_key=None):
    """
    快速识别语音（无需实例化类）
    
    Args:
        audio_path: 音频文件路径
        api_key: 阿里云百炼 API Key（可选，默认从环境变量读取）
        
    Returns:
        str: 识别的文字内容，失败返回空字符串
    """
    service = AliyunSpeechService(api_key)
    result = service.recognize(audio_path)
    return result["text"] if result["success"] else ""


if __name__ == "__main__":
    # 测试代码
    print("阿里云百炼语音识别服务")
    print("=" * 50)
    print("使用步骤：")
    print("1. 开通阿里云百炼平台：https://bailian.console.aliyun.com/")
    print("2. 获取 API Key")
    print("3. 设置环境变量：set DASHSCOPE_API_KEY=your-api-key")
    print("4. 调用 recognize_speech('audio.wav')")
    print("=" * 50)
