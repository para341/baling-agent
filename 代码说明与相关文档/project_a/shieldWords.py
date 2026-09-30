import re


def read_txt(file_name):
    # 读取txt文件
    with open(file_name, encoding='utf-8') as file_to_read:
        lines = list()
        for line in file_to_read.readlines():
            if line is not None:
                lines.append(line.strip('\n'))
    return lines


def shield_sensitive_word(text):
    # 屏蔽敏感词
    sensitive_word = read_txt("./Data/敏感词库.txt")
    for pattern in sensitive_word:
        match = re.search(pattern, text)
        if match is not None:
            text = text.replace(pattern, '~~~')
    return text