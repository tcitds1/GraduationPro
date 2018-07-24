import requests
import pickle
import re
import time
import random
import copy
import sys
import string
import re
sys.path.append('../')
from log.LogHandler import LogHandler

class WebRequests:
    def __init__(self, name):
        headers_movie = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'movie.douban.com',
            'Upgrade-Insecure-Requests': '1',
        }
        headers_user = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.douban.com',
            'Referer': 'https://www.douban.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }


        if(name=='movie'):
            self.headers = headers_movie
            self.raw_headers = headers_movie
        if(name=='user'):
            self.headers = headers_user
            self.raw_headers = headers_user

        self.test_url = 'https://movie.douban.com/subject/2334904/'
        self.log =  LogHandler('MovieRequest', file=False)
        self.forbid_count = 0
        self.redirc_count = 0
        self.change_headers = {}
        self.cookies = {}
        self.proxy = ''
        self.change_proxy()

    # 随机获取单个代理
    def get_proxy(self):
        try:
            proxy =  requests.get("http://127.0.0.1:5000/get/").text
            if(proxy == 'no proxy!'):
                return ''
            return proxy
        except Exception as e:
            return ''
    # 删除代理
    def delete_proxy(self,proxy):
        requests.get("http://127.0.0.1:5000/delete?proxy={}".format(proxy))

    def change_proxy(self):
        ua_list = [
           'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
           'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
           'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        ]
        # 随机user-agent
        ua = random.choice(ua_list)
        # 随机代理IP
        proxy = self.get_proxy()
        headers = copy.deepcopy(self.headers)
        headers['User-Agent'] = ua
        # 随机cookie bid 值
        num = ''.join(random.sample(string.digits + string.ascii_letters, 11))
        # num = '_vhor6Cwfe8'
        cookie = {'bid': num, 'll': '"118267"'}
        self.change_headers = headers
        self.proxy = proxy
        self.cookies = cookie
        # 代理不够用 先睡个5分钟再说

        # if(self.getProxyCount()<20):
        #     self.log.info('WebRequest :--{}--proxypool is not enough, send Request after sleeping 300seconds---'.format(time.ctime()))
        #     time.sleep(300)

    def sendRequest(self, url):
        # 单纯为爬取电影评论用户设置的header['Referer']
        if(re.findall('comments\?start', url)):
            self.change_headers['Referer'] = url

        proxies = {
            'http': 'http://{}'.format(self.proxy),
            'https': 'https://{}'.format(self.proxy)
        }

        try:
            if(self.proxy==''):
                self.log.info('WebRequest :--{}--未能获取到代理IP，采用真实IP进行访问---'.format(time.ctime()))
                movie_rs = requests.get(url, headers=self.raw_headers, timeout=4, allow_redirects=False)
            else:
                movie_rs = requests.get(url, headers=self.change_headers, timeout=4, proxies=proxies, cookies=self.cookies, allow_redirects=False)
            if (movie_rs.status_code == 200):
                self.forbid_count = 0
                self.redirc_count = 0
                # print('访问成功')
                return movie_rs
            elif(movie_rs.status_code == 403):
                print('访问禁止')
                return False
            elif(movie_rs.status_code ==302):
                print(url + ' 302')
                self.redirc_count +=1
                if(self.redirc_count==3):
                    return 'next'
                return False
            else:
                print(movie_rs.status_code)
                print('未知错误 请重试')
                self.forbid_count = self.forbid_count + 1
                if (self.forbid_count >= 7):
                    return 'next'
                raise Exception()
        except Exception as e:
            print(e)
            self.delete_proxy(self.proxy)
            return False

    def getProxyCount(self):
        rs = requests.get("http://127.0.0.1:5000/get_status/")
        status = rs.json()
        return status['useful_proxy']


if __name__ == '__main__':
    req = WebRequests()
    req.change_proxy()

    url = 'https://www.douban.com/people/4676959/'
    refrer = 'https://movie.douban.com/subject/1292341/comments?start=20&limit=20&sort=time&status=P&percent_type='
    rs  = req.sendRequest(url)


#     'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9,en;q=0.8

# Cookie: bid=v3FS5f6EEHg; _vwo_uuid_v2=D88EB1F3E743734411B05F0C9ED912514|7c181fce334a1b863b394bcf449c067f; ap=1; ps=y; push_noty_num=0; push_doumail_num=0; ct=y; ue="tcitds@163.com"; __utmv=30149280.17776; gr_user_id=496aac81-5609-4d9c-8a0b-30c650f7c5f7; _ga=GA1.2.1646006591.1526961902; _gid=GA1.2.673317776.1527262692; __utmz=30149280.1527265613.26.7.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); viewed="3299922_26120130_2101774"; loc-last-index-location-id="131441"; ll="131441"; __utma=30149280.1646006591.1526961902.1527317290.1527321486.30; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1527321492%2C%22https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26614893%2F%3Ffrom%3Dshowing%22%5D; _pk_ses.100001.8cb4=*; __utmt=1; __utmc=30149280; as="https://movie.douban.com/review/9393350/"; _pk_id.100001.8cb4=af2b2ac050d83f90.1508138657.132.1527322289.1527318063.; __utmb=30149280.27.9.1527321869900
# Host: www.douban.com
# Referer: https://movie.douban.com/subject/27185556/?tag=%E7%83%AD%E9%97%A8&from=gaia
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    # print(rs.text)
    # print(rs.text)
    # print(rs.status_code)

    # url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=20&genres=%E7%A7%91%E5%B9%BB'
    # for i in range(5):
    #     print(req.change_headers)
    #     print(req.cookies)
    #     print(req.proxy)
    #     req.change_proxy()

    # while True:
    #     rs = req.sendRequest(url)
    #     if(rs):
    #         print(rs.text)
    #         break
        # time.sleep(20)
