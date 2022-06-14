# -*- coding: utf-8 -*-
"""
Created on 2022-04-18 22:28:16
---------
@summary:
---------
@author: lirui
"""

import feapder
from feapder import setting
from feapder.utils.log import log
from utils.common import genpayload,genlistpayload
from items.shexchange_item import ShexchangeItem


class ShexchangeBaseParser(feapder.BaseParser):
    __custom_setting__ = dict(
        BASE_URL="http://www.sse.com.cn/",
    )

    def download_midware(self, request):
        request.headers = {
            'referer': 'http://www.sse.com.cn/',
            'Content-Type': 'multipart/form-data; boundary=wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T',
        }
        # 这里随机取个代理使用即可
        proxy_virjar = setting.get_random_proxy()
        request.proxies = {"https": proxy_virjar, "http": proxy_virjar}
        return request

    def start_requests(self):
        searchword = 'T_L CTITLE T_D E_KEYWORDS T_JT_E T_L纪要 T_RT_R'

        yield feapder.Request("http://query.sse.com.cn/search/getCountSearchResult.do?search=lmmzs", method='POST',
                              data=genlistpayload(searchword), download_midware=self.download_midware)

    def parse(self, request, response):
        result_args = response.json
        args_list = []
        for e in result_args['data']:
            args_list.append(e['word'])
        log.info(args_list)

        searchword = 'T_L CTITLE T_D E_KEYWORDS T_JT_E T_L纪要 T_R  and cchannelcode T_E T_L0T_D'
        for a in args_list:
            searchword = searchword + a + 'T_D'
        searchword = searchword + '88888888T_DT_RT_R'
        log.info(searchword)

        url = 'http://query.sse.com.cn/search/getSearchResult.do?search=qwjs'

        yield feapder.Request(url=url, method='POST', data=genpayload(searchword, 1),
                              download_midware=self.download_midware,
                              callback=self.parse_detail, searchword=searchword)

    def _sh_parse_item(self, data):
        sh_item = ShexchangeItem()
        return sh_item.load_item(data, self.__custom_setting__["BASE_URL"])

    def parse_detail(self, request, response):
        url = request.url
        searchword = request.searchword

        result_data = response.json
        countpage = result_data['countPage']
        data = result_data['data']

        for e in data:
            sh_item = self._sh_parse_item(e)
            log.info(f'sh_item:{sh_item}')
            yield sh_item

        for i in range(2, int(countpage) + 1):
            yield feapder.Request(url=url, method='POST', data=genpayload(searchword, i),
                                  download_midware=self.download_midware,
                                  callback=self.parse_item)

    def parse_item(self, request, response):
        result_data = response.json
        data = result_data['data']

        for e in data:
            sh_item = self._sh_parse_item(e)
            log.info(f'sh_item:{sh_item}')
            yield sh_item


if __name__ == "__main__":
    ShexchangeMysql(5).start()