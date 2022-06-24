from feapder import setting
import os
from utils.common import parse_html


if __name__ == "__main__":
    if not os.path.exists(setting.XUEQIU_PARSER_PATH):
        os.makedirs(setting.XUEQIU_PARSER_PATH)
    print(__file__)

    for dirpath, dirnames, filenames in os.walk(setting.XUEQIU_DOWNLOAD_PATH):
        for filename in filenames:
            '''
            dirpath是文件夹路径
            dirnames是文件夹名称
            filenames是文件名称
            '''
            file_path = os.path.join(dirpath, filename)
            with open(file_path,'r') as f:
                content = f.read()
                text = parse_html(content)
            print(f'已读取{file_path}')

            parserfile_path = os.path.join(setting.XUEQIU_PARSER_PATH, filename)
            with open(parserfile_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'已清洗{parserfile_path}')