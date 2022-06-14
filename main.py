# -*- coding: utf-8 -*-
"""
Created on 2022-04-03 21:22:28
---------
@summary: 爬虫入口
---------
@author: lirui
"""

from feapder import ArgumentParser

from spiders import szexchange_airspider,shexchange_airspider,xueqiu_airspider,xueqiu_spider,szexchange_batchspider

def crawl_szexchange_airspider():
    """
    AirSpider爬虫：深圳交易所纪要文章爬虫
    """
    spider = szexchange_airspider.Szexchange(thread_count=5)
    spider.start()

def crawl_shexchange_airspider():
    """
    AirSpider爬虫：上海交易所纪要文章爬虫
    """
    spider = shexchange_airspider.Shexchange(thread_count=10)
    spider.start()

def crawl_xueqiu_airspider():
    """
    AirSpider爬虫：雪球纪要文章爬虫
    """
    spider = xueqiu_airspider.Xueqiu(thread_count=15)
    spider.start()

def crawl_xueqiu_mysql():
    """
    Spider爬虫：分布式雪球纪要文章爬虫
    """
    spider = xueqiu_spider.XueqiuMysql(search_keyword='纪要', thread_count=10, redis_key="xueqiu:spider")
    spider.start()


def crawl_batch_szexchange(args):
    """
    BatchSpider爬虫：周期深圳交易所纪要文章爬虫
    """
    spider = szexchange_batchspider.BatchSzexchange(
        redis_key="szexchange:task",  # redis中存放任务等信息的根key
        task_table="szexchange_spider_task",  # mysql中的任务表
        task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段
        batch_record_table="batch_szexchange_spider_record",  # mysql中的批次记录表
        batch_name="批次爬虫测试(周全)",  # 批次名字
        batch_interval=7,  # 批次周期 天为单位 若为小时 可写 1 / 24
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == 3:
        spider.init_task()


if __name__ == "__main__":
    parser = ArgumentParser(description="纪要文章爬虫")

    parser.add_argument(
        "--crawl_szexchange_airspider", action="store_true", help="深圳交易所纪要爬虫", function=crawl_szexchange_airspider
    )
    parser.add_argument(
        "--crawl_shexchange_airspider", action="store_true", help="上海交易所纪要爬虫", function=crawl_shexchange_airspider
    )
    parser.add_argument(
        "--crawl_xueqiu_airspider", action="store_true", help="雪球纪要爬虫", function=crawl_xueqiu_airspider
    )
    # parser.add_argument(
    #     "--crawl_xueqiu_mysql", action="store_true", help="分布式雪球纪要爬虫", function=crawl_xueqiu_mysql
    # )
    # parser.add_argument(
    #     "--crawl_batch_szexchange",
    #     type=int,
    #     nargs=1,
    #     help="周期深圳交易所纪要爬虫",
    #     choices=[1, 2, 3],
    #     function=crawl_batch_szexchange,
    # )

    parser.start()

    # main.py作为爬虫启动的统一入口，提供命令行的方式启动多个爬虫，若只有一个爬虫，可不编写main.py
    # 将上面的xxx修改为自己实际的爬虫名
    # 查看运行命令 python main.py --help
    # AirSpider与Spider爬虫运行方式 python main.py --crawl_xxx
    # BatchSpider运行方式
    # 1. 下发任务：python main.py --crawl_xxx 1
    # 2. 采集：python main.py --crawl_xxx 2
    # 3. 重置任务：python main.py --crawl_xxx 3

