# -*- coding: utf-8 -*-
"""
Created on 2022-04-12 22:35:26
---------
@summary:
---------
@author: lirui
"""

from feapder import Item
import time, farmhash, lzma, re, datetime, os
from urllib import parse
from feapder import setting
from feapder.utils.log import log


class XueqiuItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i xueqiu
    """

    __table_name__ = "xueqiu"
    __unique_key__ = ["url","urlhash"]

    def __init__(self, *args, **kwargs):
        # self.id = None
        self.created_at = None
        self.description = None
        self.like_count = None
        self.reply_count = None
        self.retweet_count = None
        self.url = None
        self.urlhash = None
        self.text = None
        self.title = None
        self.user_name = None
        self.user_id = None
        self.view_count = None
        self.time = None
        self.downloaded = None

    def load_item(self, data, base_url):
        pattern = re.compile(r'<[^>]+>', re.S)
        description = pattern.sub('', data.get('description'))
        title = pattern.sub('', data.get('title'))

        createdArray = time.localtime(data['created_at'] / 1000)
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", createdArray)
        url = parse.urljoin(base_url, data.get('target'))
        self.created_at = created_at

        self.description = description
        self.like_count = data.get('like_count')
        self.reply_count = data.get('reply_count')
        self.retweet_count = data.get('retweet_count')
        self.url = url
        self.urlhash = farmhash.hash64(url)
        self.text = lzma.compress(data.get('text').encode('utf8'))
        self.title = title
        self.user_name = data.get('user').get('screen_name')
        self.user_id = data.get('user_id')
        self.view_count = data.get('view_count')
        self.time = datetime.datetime.now()
        return self

    def download_file(self, data):
        file = data.get('target').replace('/','_')
        title = self.title.replace('/','_')
        user_name = self.user_name.replace('/','_')

        file_path = os.path.join(setting.XUEQIU_DOWNLOAD_PATH, title + '-' + user_name + file + '.txt')
        log.info(f"此时的file_path:{file_path}")

        if self.downloaded == 0:
            try:
                with open(file_path,'w') as f:
                    f.write(data.get('text'))
                log.info(f"该文件下载成功:{self.url}")
                self.downloaded = 1
            except Exception as e:
                log.info(f"该文件下载有问题:{self.url}")
                log.info(f"{e}")
                self.downloaded = 0
        else:
            log.info(f"该文件已经下载:{self.url}")

