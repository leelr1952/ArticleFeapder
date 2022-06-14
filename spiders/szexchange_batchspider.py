# -*- coding: utf-8 -*-
"""
Created on 2022-04-25 23:03:25
---------
@summary:
---------
@author: lirui
"""

import feapder, random, math
from feapder import setting, ArgumentParser
from items.szexchange_item import SzexchangeItem
from feapder.utils.log import log


class BatchSzexchange(feapder.BatchSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        BASE_URL='http://www.szse.cn',
        PAGE_SIZE=20
    )

    def download_midware(self, request):
        # 这里随机取个代理使用即可
        proxy_virjar = setting.get_random_proxy()
        request.proxies = {"https": proxy_virjar, "http": proxy_virjar}
        return request

    def start_requests(self, task):
        id, url = task  # id， url为所取的字段，main函数中指定的
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
        yield feapder.Request(url, task_id=id, params=params, data=data, verify=False, method="POST")

    def _sz_parse_item(self, data):
        sz_item = SzexchangeItem()
        return sz_item.load_item(data, self.__custom_setting__["BASE_URL"])

    def parse(self, request, response):
        result_data = response.json
        for data in result_data['data']:
            sz_item = self._sz_parse_item(data)
            log.info(f'sz_item:{sz_item}')
            yield sz_item
        yield self.update_task_batch(request.task_id, 1)  # 更新任务状态为1

        totalsize = result_data['totalSize']
        totalpage = math.ceil(totalsize / 20)
        for i in range(2, totalpage + 1):
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
            yield feapder.Request(request.url, params=params, data=data, verify=False, method="POST",
                                  callback=self.parse_items)

    def parse_items(self, request, response):
        result_data = response.json
        for data in result_data['data']:
            sz_item = self._sz_parse_item(data)
            log.info(f'sz_item:{sz_item}')
            yield sz_item
        # yield self.update_task_batch(request.task_id, 1)  # 更新任务状态为1

    def failed_request(self, request, response):
        """
        @summary: 超过最大重试次数的request
        ---------
        @param request:
        ---------
        @result: request / item / callback / None (返回值必须可迭代)
        """

        yield request
        yield self.update_task_batch(request.task_id, -1)  # 更新任务状态为-1


def crawl_batch_szexchange(args):
    spider = BatchSzexchange(
        redis_key="szexchange:task",  # redis中存放任务等信息的根key
        task_table="szexchange_spider_task",  # mysql中的任务表
        task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="batch_szexchange_spider_record",  # mysql中的批次记录表
        batch_name="批次爬虫测试(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    if args == 1:
        spider.start_monitor_task()  # 下发及监控任务
    else:
        spider.start()  # 采集


if __name__ == "__main__":
    parser = ArgumentParser(description="批次爬虫-深圳交易所")

    parser.add_argument(
        "--crawl_batch_szexchange", type=int, nargs=1, help="(1|2）", function=crawl_batch_szexchange
    )
    # parser.add_argument("--test_debug", action="store_true", help="测试debug", function=test_debug)

    parser.start()

    # 下发任务及监控进度 python3 main.py --crawl_test 1
    # 采集 python3 main.py --crawl_test 2
