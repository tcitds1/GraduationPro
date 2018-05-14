
import sys
from multiprocessing import Process

sys.path.append('../')

# from Api.ProxyApi import run as ProxyApiRun
from ProxyValidSchedule import run as ValidRun
from ProxyRefreshSchedule import run as RefreshRun

def run():
    p_list = list()
    p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
    p_list.append(p1)
    p2 = Process(target=ValidRun, name='ValidRun')
    p_list.append(p2)
    p3 = Process(target=RefreshRun, name='RefreshRun')
    p_list.append(p3)

    for p in p_list:
        # 主进程退出时不检查子进程直接退出
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()


if __name__ == '__main__':
    run()
