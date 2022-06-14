# -*- coding: utf-8 -*-
"""
Created on 2022-04-12 22:36:18
---------
@summary:
---------
@author: lirui
"""

import feapder
from feapder import setting
from feapder.utils.tools import get_cookies
from urllib import parse
from feapder.utils.log import log
from items.xueqiu_item import XueqiuItem
from utils.cookie_pool import xueqiu_cookie_pool


class XueqiuMysql(feapder.Spider):
    __custom_setting__ = dict(
        XUEQIU_BASE_URL = 'https://xueqiu.com'
    )

    def __init__(self, search_keyword, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.XUEQIU_SEARCH_KEYWORD_Q = parse.quote(search_keyword)

    def download_midware(self, request):
        # 这里随机取个代理使用即可
        proxy_virjar = setting.get_random_proxy()
        request.proxies = {"https": proxy_virjar, "http": proxy_virjar}
        return request

    def start_requests(self):
        # yield feapder.Request("https://xueqiu.com")
        xueqiu_cookie1 = xueqiu_cookie_pool.get_user()
        xueqiu_cookie2 = xueqiu_cookie_pool.get_user()
        log.debug(xueqiu_cookie1)
        log.debug(xueqiu_cookie2)
        status_url = f'https://xueqiu.com/query/v1/search/status.json?sortId=1&q={self.XUEQIU_SEARCH_KEYWORD_Q}&count=20&page=1'
        yield feapder.Request(status_url, cookies=xueqiu_cookie1.cookies, callback=self.parse_status_url,
                              download_midware=self.download_midware,user_id = xueqiu_cookie1.user_id)

        user_url = f'https://xueqiu.com/query/v1/search/user.json?q={self.XUEQIU_SEARCH_KEYWORD_Q}&count=20&page=1'
        yield feapder.Request(user_url, cookies=xueqiu_cookie2.cookies, callback=self.parse_user_url,
                              download_midware=self.download_midware,user_id = xueqiu_cookie2.user_id)

    def parse_status_url(self, request, response):
        response_data = response.json
        maxPage = response_data['maxPage']
        status_urls = [
            f'https://xueqiu.com/query/v1/search/status.json?sortId=1&q={self.XUEQIU_SEARCH_KEYWORD_Q}&count=20&page={_page}'
            for _page in range(1, maxPage + 1)]
        for url in status_urls:
            yield feapder.Request(url, callback=self.parse_status_detail, cookies=request.cookies)

    def parse_status_detail(self, request, response):
        response_data = response.json
        if response_data['count'] == 0:
            log.info(f"该{response.url}没有数据")
            return None

        else:
            for data in response_data['list']:
                xueqiu_item = self._xueqiu_parse_item(data)
                log.info(f'xueqiu_item:{xueqiu_item}')
                yield xueqiu_item

    def _xueqiu_parse_item(self, data):
        xueqiu_item = XueqiuItem()
        xueqiu_item.load_item(data, self.__custom_setting__['XUEQIU_BASE_URL'])
        return xueqiu_item

    def parse_user_url(self, request, response):
        response_data = response.json
        maxPage = response_data['maxPage']
        user_urls = [
            f'https://xueqiu.com/query/v1/search/user.json?q={self.XUEQIU_SEARCH_KEYWORD_Q}&count=20&page={_page}'
            for _page in range(1, maxPage + 1)
        ]
        for url in user_urls:
            yield feapder.Request(url, callback=self.parse_user_list, cookies=request.cookies)

    def parse_user_list(self, request, response):
        response_data = response.json

        for data in response_data['list']:
            user_id = data['id']
            user_url = f'https://xueqiu.com/query/v1/user/status/search.json?q={self.XUEQIU_SEARCH_KEYWORD_Q}&page=1&uid={user_id}&sort=time&comment=0'
            yield feapder.Request(user_url, callback=self.parse_user_status_url, dont_filter=True, cookies=request.cookies)

    def parse_user_status_url(self, request, response):
        response_data = response.json
        maxPage = response_data['maxPage']

        if response_data['count'] == 0:
            log.info(f"该{response.url}没有数据")
            return None
        else:
            for data in response_data['list']:
                user_id = data['user_id']

                user_keyword_urls = [
                    f'https://xueqiu.com/query/v1/user/status/search.json?q={self.XUEQIU_SEARCH_KEYWORD_Q}&page={_page}&uid={user_id}&sort=time&comment=0'
                    for _page in range(1, maxPage+1)
                ]

                for url in user_keyword_urls:
                    yield feapder.Request(url, callback=self.parse_user_keyword_detail, cookies=request.cookies)

    def parse_user_keyword_detail(self, request, response):
        response_data = response.json
        if response_data['count'] == 0:
            log.info(f"该{response.url}没有数据")
            return None

        else:
            for data in response_data['list']:
                xueqiu_item = self._xueqiu_parse_item(data)
                log.info(f'xueqiu_item:{xueqiu_item}')
                yield xueqiu_item

    def validate(self, request, response):
        if request.callback_name == 'parse_user_url' or request.callback_name == 'parse_user_url':
            if response.status_code == 200:
                user_id = request.user_id
                xueqiu_cookie_pool.del_user(user_id)


if __name__ == "__main__":
    XueqiuMysql(search_keyword='纪要',thread_count=10,redis_key="xueqiu:spider").start()