import os
from datetime import datetime


#日志类
class Logger:

    def __init__(self, mode=0):
        self.mode = mode
        if mode == 1:
            if os.path.exists('./logs/info.log'):
                if os.path.getsize('./logs/info.log') / 1024 > 32:
                    os.remove('./logs/info.log')

    def info(self, content):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[LOG]" + " " + now + " " + content)
        if self.mode == 1:
            with open('./logs/info.log', 'a') as f:
                f.write("[LOG]" + " " + now + "" + content + '\n')
