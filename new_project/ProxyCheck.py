# -*- coding: utf-8 -*-
__author__ = 'J_hao'

import sys
from threading import Thread

sys.path.append('../')

from utilFunction import validUsefulProxy
from ProxyManager import ProxyManager
from log.LogHandler import LogHandler

FAIL_COUNT = 1  # 校验失败次数， 超过次数删除代理


class ProxyCheck(ProxyManager, Thread):
    def __init__(self, queue, item_dict):
        ProxyManager.__init__(self)
        Thread.__init__(self)
        self.log = LogHandler('proxy_check', file=False)  # 多线程同时写一个日志文件会有问题
        self.queue = queue
        self.item_dict = item_dict

    def run(self):
        self.db.changeTable(self.useful_proxy_queue)
        while self.queue.qsize():
            proxy = self.queue.get()
            count = self.item_dict[proxy]
            if validUsefulProxy(proxy):
                # 验证通过计数器减1
                if int(count) > 0:
                    # self.db.update(proxy, num=int(count) - 1)
                    pass
                else:
                    pass
                self.log.info('ProxyCheck: {} validation pass'.format(proxy))
            else:
                self.log.info('ProxyCheck: {} validation fail'.format(proxy))
                if int(count) + 1 >= FAIL_COUNT:
                    self.log.info('ProxyCheck: {} fail too many, delete!'.format(proxy))
                    self.db.delete(proxy)
                else:
                    self.db.update(proxy, num=int(count) + 1)
            self.queue.task_done()


if __name__ == '__main__':
    # p = ProxyCheck()
    # p.run()
    pass
