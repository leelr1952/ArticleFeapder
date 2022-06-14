import feapder, random, math, os
from feapder import setting
from items.szexchange_item import SzexchangeItem
from feapder.utils.log import log


class Szexchange(feapder.AirSpider):
    __custom_setting__ = dict(
        BASE_URL = 'http://www.szse.cn',
        PAGE_SIZE = 20
    )

    def download_midware(self, request):
        # 这里随机取个代理使用即可
        proxy_virjar = setting.get_random_proxy()
        request.proxies = {"https": proxy_virjar, "http": proxy_virjar}
        return request

    def start_requests(self):
        if not os.path.exists(setting.SZ_DOWNLOAD_PATH):
            os.makedirs(setting.SZ_DOWNLOAD_PATH)

        url = "http://www.szse.cn/api/search/content"
        params = {
            "random": random.random()
        }
        data = {
            "keyword": "纪要",
            "range": "title",
            "time": "1",
            "orderby": "score",
            "currentPage": "1",
            "pageSize": self.__custom_setting__['PAGE_SIZE'],
            "openChange": "true"
        }
        yield feapder.Request(url, params=params, data=data, verify=False, method="POST")

    def _sz_parse_item(self, data):
        sz_item = SzexchangeItem()
        return sz_item.load_item(data, self.__custom_setting__["BASE_URL"])

    def parse(self, request, response):
        result_data = response.json
        for data in result_data['data']:
            sz_item = self._sz_parse_item(data)
            log.info(f'sz_item:{sz_item}')
            sz_item.download_file(data)

            if sz_item["pdf_name"] is None or not sz_item["pdf_name"] or sz_item["pdf_name"] == '':
                yield feapder.Request(sz_item.jsonurl, verify=False, callback=self.parse_jsonurl,sz_item=sz_item)
            yield sz_item

        totalsize = result_data['totalSize']
        totalpage = math.ceil(totalsize / 20)
        for i in range(2, totalpage+1):
            params = {
                "random": random.random()
            }
            data = {
                "keyword": "纪要",
                "range": "title",
                "time": "1",
                "orderby": "score",
                "currentPage": str(i),
                "pageSize": "20",
                "openChange": "true"
            }
            yield feapder.Request(request.url, params=params, data=data, verify=False, method="POST", callback=self.parse_items)

    def parse_items(self, request, response):
        result_data = response.json
        for data in result_data['data']:
            sz_item = self._sz_parse_item(data)
            log.info(f'sz_item:{sz_item}')
            sz_item.download_file(data)

            if sz_item["pdf_name"] is None or not sz_item["pdf_name"] or sz_item["pdf_name"] == '':
                yield feapder.Request(sz_item.jsonurl, verify=False, callback=self.parse_jsonurl,sz_item=sz_item)

            yield sz_item

    def parse_jsonurl(self, request, response):
        result_data = response.json
        if result_data['message'] == '成功':
            content = result_data['data']['content']

            filename = os.path.join(setting.SZ_DOWNLOAD_PATH, result_data["data"]["title"] + '.txt')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            log.info(f"jsonurl文件写入成功:{filename}")
            request.sz_item.downloaded = 1
            yield request.sz_item
        else:
            log.error(f"请求jsonurl出错:{request.url}")
            raise Exception(f"请求jsonurl出错:{request.url}")


if __name__ == "__main__":
    Szexchange(thread_count=5).start()
