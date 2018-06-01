# -*- coding: utf-8 -*-

import sys
import time
import pickle

from queue import Queue  # py2
sys.path.append('../')

from ProxyCheck import ProxyCheck
from ProxyManager import ProxyManager


class ProxyValidSchedule(ProxyManager, object):
    def __init__(self):
        ProxyManager.__init__(self)
        self.queue = Queue()
        self.proxy_item = dict()

    def __validProxy(self, threads=10):
        # 验证useful_proxy代理
        thread_list = list()
        for index in range(threads):
            thread_list.append(ProxyCheck(self.queue, self.proxy_item))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def putQueue(self):
        self.db.changeTable(self.useful_proxy_queue)
        self.proxy_item = self.db.getAll()
        for item in self.proxy_item:
            self.queue.put(item)

    def main(self):
        self.putQueue()
        while True:
            if not self.queue.empty():
                self.log.info("Start valid useful proxy")
                self.__validProxy()

            else:
                self.log.info('Valid Complete! sleep 40 seconds.')
                time.sleep(40)
                self.putQueue()


def run():
    p = ProxyValidSchedule()
    p.main()

if __name__ == '__main__':
    p = ProxyValidSchedule()
    p.main()
    # useful_pool_status = p.getPoolStatus('useful_proxy')
    # with open('../useful_pool_status', 'wb') as f:
    #     pickle.dump(useful_pool_status, f)
    # p.main()
