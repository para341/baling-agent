import os

import requests
import json

class DeepSeekService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.endpoint = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"

    def chat(self, message):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个B站弹幕智能预警系统的AI助手，负责回答用户关于弹幕分析、网络环境优化等方面的问题。"},
                {"role": "user", "content": message}
            ],
            "stream": False
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"连接 DeepSeek 出错: {str(e)}"

llm_service = DeepSeekService()
