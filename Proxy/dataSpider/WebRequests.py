import requests
import pickle
import re
import time
import random
import copy
import sys
import string

class WebRequests:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/tag/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101'
        }
        self.test_url = 'https://movie.douban.com/subject/2334904/'

    # 随机获取单个代理
    def get_proxy(self):
        return requests.get("http://127.0.0.1:5000/get/")

    # 删除代理
    def delete_proxy(self,proxy):
        requests.get("http://127.0.0.1:5000/delete?proxy={}".format(proxy))

    def sendRequest(self, url):
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        ua = random.choice(ua_list)
        proxy = self.get_proxy().text
        proxies = {
            'http': 'http://{}'.format(proxy),
        }
        headers = copy.deepcopy(self.headers)
        headers['User-Agent'] = ua
        num = ''.join(random.sample(string.digits + string.ascii_letters, 11))
        # num = '_vhor6Cwfe8'
        cookie = {'bid': num, 'll': '"118267"'}

        # print(url)
        # print(proxies)
        try:
            movie_rs = requests.get(url, timeout=4, proxies=proxies, cookies=cookie)
            if (movie_rs.status_code == 200):
                print('访问成功')
                return movie_rs
            elif(movie_rs.status_code == 403):
                print('访问禁止')
                return False
            else:
                print(movie_rs.status_code)
                print('未知错误 请重试')
                raise Exception()
        except Exception as e:
            print(e)
            # self.delete_proxy(proxy)
            # print('已删除代理{}'.format(proxy))
            time.sleep(2)
            return False

if __name__ == '__main__':
    req = WebRequests()
    url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=20&genres=%E7%A7%91%E5%B9%BB'
    req.sendRequest(url)
    # while True:
    #     rs = req.sendRequest(url)
    #     if(rs):
    #         print(rs.text)
    #         break
        # time.sleep(20)
