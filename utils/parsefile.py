from feapder import setting
import os
from utils.common import parse_html


def parse_file(src_path, dst_path):
    for dirpath, dirnames, filenames in os.walk(src_path):
        for filename in filenames:
            '''
            dirpath是文件夹路径
            dirnames是文件夹名称
            filenames是文件名称
            '''
            if filename.endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                    text = parse_html(content)
                print(f'已读取{file_path}')

                parserfile_path = os.path.join(dst_path, filename)
                with open(parserfile_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f'已清洗{parserfile_path}')
            else:
                print(f'{filename}不是txt，考虑其他方式')


if __name__ == "__main__":
    if not os.path.exists(setting.XUEQIU_PARSER_PATH):
        os.makedirs(setting.XUEQIU_PARSER_PATH)
    if not os.path.exists(setting.SZ_PARSER_PATH):
        os.makedirs(setting.SZ_PARSER_PATH)
    if not os.path.exists(setting.SH_PARSER_PATH):
        os.makedirs(setting.SH_PARSER_PATH)

    parse_file(setting.SH_DOWNLOAD_PATH, setting.SH_PARSER_PATH)
    parse_file(setting.SZ_DOWNLOAD_PATH, setting.SZ_PARSER_PATH)
    parse_file(setting.XUEQIU_DOWNLOAD_PATH, setting.XUEQIU_PARSER_PATH)

