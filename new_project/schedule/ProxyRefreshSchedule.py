# -*- coding: utf-8 -*-
import sys
import time
import logging
from threading import Thread
from apscheduler.schedulers.blocking import BlockingScheduler
import pickle
sys.path.append('../')

from utilFunction import validUsefulProxy
from ProxyManager import ProxyManager
from log.LogHandler import LogHandler

logging.basicConfig()


class ProxyRefreshSchedule(ProxyManager):
    """
    代理定时刷新
    """
    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('refresh_schedule')

    def validProxy(self):
        """
        验证raw_proxy_queue中的代理, 将可用的代理放入useful_proxy_queue
        :return:
        """
        self.db.changeTable(self.raw_proxy_queue)
        raw_proxy_item = self.db.pop()
        self.log.info('ProxyRefreshSchedule: %s 开启验证线程' % time.ctime())
        # 计算剩余代理，用来减少重复计算
        remaining_proxies = self.getAll()
        while raw_proxy_item:
            # proxy
            raw_proxy = raw_proxy_item.get('proxy')
            # from
            from_method = raw_proxy_item.get('from')

            if (raw_proxy not in remaining_proxies) and validUsefulProxy(raw_proxy):
                self.db.changeTable(self.useful_proxy_queue)
                self.db.put(raw_proxy, from_method)
                self.log.info('ProxyRefreshSchedule: %s validation pass' % raw_proxy)
            else:
                self.log.info('ProxyRefreshSchedule: %s validation fail' % raw_proxy)
            self.db.changeTable(self.raw_proxy_queue)
            raw_proxy_item = self.db.pop()
            remaining_proxies = self.getAll()
        self.log.info('ProxyRefreshSchedule: %s 当前线程验证完毕' % time.ctime())

def refreshPool():
    pp = ProxyRefreshSchedule()
    pp.validProxy()

def main(process_num=5):
    p = ProxyRefreshSchedule()
    # 获取新代理
    p.refresh()
    # 将原生代理池状态储存
    raw_pool_status = p.getPoolStatus('raw_proxy')
    if(raw_pool_status):
        with open('../raw_pool_status', 'wb') as f:
            pickle.dump(raw_pool_status, f)
    # 检验新代理
    pl = []
    for num in range(process_num):
        proc = Thread(target=refreshPool, args=())
        pl.append(proc)

    for num in range(process_num):
        pl[num].daemon = True
        pl[num].start()

    for num in range(process_num):
        pl[num].join()
    print('当前代理IP爬取进程结束，请等待下一次爬取')
def run():
    main()
    sch = BlockingScheduler()
    sch.add_job(main, 'interval', seconds=6)  # 每5s抓取一次
    sch.start()

if __name__ == '__main__':
    run()
