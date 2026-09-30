# 读取txt文件
def read_txt(file_name):
    with open(file_name, encoding='utf-8') as file_to_read:
        lines = list()
        for line in file_to_read.readlines():
            if line is not None:
                lines.append(line.strip('\n'))
    return lines