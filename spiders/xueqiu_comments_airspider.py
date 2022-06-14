# -*- coding: utf-8 -*-
"""
Created on 2022-05-17 21:53:06
---------
@summary:
---------
@author: lirui
"""

import feapder
from feapder import setting
from feapder.utils.tools import get_cookies
from feapder.utils.log import log
from items.xueqiu_item import XueqiuItem
from urllib import parse


class XueqiuCommentsAirspider(feapder.AirSpider):
    __custom_setting__ = dict(
        XUEQIU_BASE_URL='https://xueqiu.com',
        XUEQIU_SEARCH_KEYWORD_Q = parse.quote('纪要')
    )

    def start_requests(self):
        yield feapder.Request(self.__custom_setting__['XUEQIU_BASE_URL'])

    def download_midware(self, request):
        # 这里随机取个代理使用即可
        proxy_virjar = setting.get_random_proxy()
        request.proxies = {"https": proxy_virjar, "http": proxy_virjar}
        return request

    def parse(self, request, response):
        cookies = get_cookies(response)

        status_url = f'https://xueqiu.com/query/v1/search/status.json?sortId=1&q={self.__custom_setting__["XUEQIU_SEARCH_KEYWORD_Q"]}&count=20&page=1'
        yield feapder.Request(status_url, cookies=cookies, callback=self.parse_status_url, dont_filter=True)

    def parse_status_url(self, request, response):
        response_data = response.json
        maxPage = response_data['maxPage']
        status_urls = [
            f'https://xueqiu.com/query/v1/search/status.json?sortId=1&q={self.__custom_setting__["XUEQIU_SEARCH_KEYWORD_Q"]}&count=20&page={_page}'
            for _page in range(1, maxPage + 1)]
        for url in status_urls:
            yield feapder.Request(url, callback=self.parse_status_detail, cookies=request.cookies)

    def parse_status_detail(self, request, response):
        if response is None or response.status_code != 200:
            log.error(f"非法页面:{request.url}")
            raise Exception(f"非法页面:{request.url}")
        else:
            response_data = response.json

            if response_data['count'] == 0:
                log.info(f"该{response.url}没有数据")
                return None

            else:
                for data in response_data['list']:
                    # with open('data6.txt', 'a+') as f:
                    #     f.write(data['target'])
                    #     f.write('\n')
                    xueqiu_item = self._xueqiu_parse_item(data)
                    log.info(f'xueqiu_item:{xueqiu_item}')
                    yield xueqiu_item

    def exception_request(self, request, response):
        """
        @summary: 请求或者parser里解析出异常的request
        ---------
        @param request:
        @param response:
        ---------
        @result: request / callback / None (返回值必须可迭代)
        """
        log.error(f"进入request异常:{request.url},当前重试次数:{request.retry_times},当前代理:{request.proxies}")
        proxy_virjar = setting.get_random_proxy()
        request.proxies = {"https": proxy_virjar, "http": proxy_virjar}
        log.error(f"切换request代理：{request.proxies}")
        yield request

    def _xueqiu_parse_item(self, data):
        xueqiu_item = XueqiuItem()
        loaded_xueqiu_item = xueqiu_item.load_item(data, self.__custom_setting__['XUEQIU_BASE_URL'])
        return loaded_xueqiu_item



if __name__ == "__main__":
    XueqiuCommentsAirspider(thread_count=10).start()