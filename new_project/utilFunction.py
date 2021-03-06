# -*- coding: utf-8 -*-

import requests
import time
from lxml import etree
from log.LogHandler import LogHandler
from webRequest.webRequest import WebRequest

logger = LogHandler(__name__, file=False)


# noinspection PyPep8Naming
def verifyProxyFormat(proxy):
    # 检查代理格式
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False

def validUsefulProxy(proxy):
    # 检查代理是否可用
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过10秒的代理就不要了
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5, verify=False)
        if r.status_code == 200:
            return True
    except Exception as e:
        logger.error(str(e))
        return False


# noinspection PyPep8Naming
def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    wr = WebRequest()

    # delay 2s for per request
    time.sleep(2)

    html = wr.get(url=url, header=header).content
    return etree.HTML(html)




def test():
    validUsefulProxy('123.122.22.77:1999')

