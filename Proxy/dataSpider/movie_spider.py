import requests
import pickle
import re
import time
import random
import copy
import sys
from threading import Thread
from lxml import etree
from WebRequests import WebRequests
sys.path.append('../')
from database.MongoDbMovie import MongoDbMovie
from log.LogHandler import LogHandler

class MovieSpider(object):

    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'movie.douban.com',
            'Referer': 'https://movie.douban.com/tag/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        self.webRequests = WebRequests()
        self.get = self.webRequests.sendRequest
        self.db = MongoDbMovie('localhost', 27017)

    def spider_movie(self, movie_tag_url):
        start = 0
        url = movie_tag_url.format(start)
        while True:
            while True:
                response = self.get(url)
                if(response):
                    break
            print('get movie url links,access right')
            data_array = (response.json())['data']
            if(len(data_array)==0)
                break
            for data in data_array:
                if self.db.exists(data['title']):
                    continue
                self.analyse_page(data)
            start = start + 20
            url = movie_tag_url.format(start)

    def analyse_page(self, movie_page_data):
        data = dict()
        movie_page_url = movie_page_data['url']
        while True:
            response = self.get(movie_page_url)
            if (response):
                break
        response = response.text
        movie_tree = etree.HTML(response)
        try:
            data['movie_title'] = movie_page_data['title']
            data['movie_rate'] = movie_page_data['rate']
            data['movie_directors'] = movie_page_data['directors']
            data['movie_url'] = movie_page_data['url']
            data['movie_casts'] = movie_page_data['casts']
            data['movie_photo'] = movie_page_data['cover']
            data['movie_id'] = movie_page_data['id']
            # 年份
            year = movie_tree.xpath('//span[@class="year"]/text()')[0]
            data['year'] = ''.join(list(year)[1:-1])
            # 电影类型
            data['movie_types'] = movie_tree.xpath('//span[@property="v:genre"]/text()')
            # 编剧
            data['movie_sw'] = movie_tree.xpath('//div[@id="info"]/span[position()=2]/span[@class="attrs"]/a/text()')
            # 语言
            regex_lang = r"(?<=语言:<\/span>).*?(?=<br\/>)"
            data['movie_langs'] = re.findall(regex_lang, response)[0].replace(' ', '').split('/')
            # 制片国家
            regex_area = r"(?<=制片国家\/地区:<\/span>).*?(?=<br\/>)"
            data['movie_areas'] = re.findall(regex_area, response)[0].replace(' ', '').split('/')
            # 时长
            try:
                movie_time = movie_tree.xpath('//span[@property="v:runtime"]/text()')[0].replace(' ','')
            except:
                data['movie_time'] = 'unknow'
            # 多少人标记看过
            regex_watched = r"\d+人看过"
            movie_watched = re.findall(regex_watched, response)[0].replace('人看过','')
            data['movie_watched'] = int(movie_watched)
            # 影片标签
            data['movie_tags'] = movie_tree.xpath('//div[@class="tags-body"]/a/text()')
        except Exception as e:
            print(e)
        print(" {} 已存储".format(data['movie_title']))
        self.db.put(data)

    def test(self):
        start = time.time()
        'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=fbfc504c469c4c669cbe57a8b220e64c&count=5&expiryDate=0&format=1&newLine=2'

        # r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)

        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=40&genres=%E5%89%A7%E6%83%85'
        url1 = 'https://www.zhihu.com/'
        url2 = 'https://movie.douban.com/subject/2334904/'
        start = 40

        while (True):
            rs = self.get(url)
            if(rs):
                print(rs.json())
            else:
                print('dailibuxing')
                break
            start = start + 20
            url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}&genres=%E5%89%A7%E6%83%85'.format(start)
            time.sleep(5)
        end = time.time()
        print('spend {} times'.format(end-start))

def main():

    tag_list = ['剧情', '喜剧', '动作', '爱情', '科幻', '悬疑', '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记',
                '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠', '情色']
    tag_url_list = list()
    # 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=10000&genres=爱情'
    tag_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}&genres={}'
    for i in tag_list:
        total_url = tag_url.format('{}', i)
        tag_url_list.append(total_url)
    pl = []


    for num in range(process_num):
        proc = Thread(target=refreshPool, args=())
        pl.append(proc)

    for num in range(process_num):
        pl[num].daemon = True
        pl[num].start()

    for num in range(process_num):
        pl[num].join()


if __name__ == "__main__":
    spider = MovieSpider()
    movie_tag_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}&genres=%E5%89%A7%E6%83%85'
    spider.spider_movie(movie_tag_url)
    example = '''
    1.如果不能访问，更换user-agent和proxy
    2.已经存在的数据： 导演 主演 分数 电影名字
    3.需要爬取得数据： 年份 影片类型  编剧 制片国家地区 语言s 多少人标记想看 影片标签 片长 
    {
        'directors': ['马丁·斯科塞斯'], 
        'rate': '8.7', 'cover_x': 2480, 
        'star': '45', 'title': '禁闭岛', 
        'url': 'https://movie.douban.com/subject/2334904/', 
        'casts': ['莱昂纳多·迪卡普里奥', '马克·鲁弗洛', '本·金斯利', '马克斯·冯·叙多夫', '米歇尔·威廉姆斯'], 
        'cover': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1832875827.jpg', 
        'id': '2334904', 
        'cover_y': 3543
    }
    '''
    # def save_data(self):
    #     url = 'https://movie.douban.com/subject/2334904/'
    #     response = requests.get(url, headers=self.headers)
    #     if (response.status_code == 200):
    #         with open('movie_data', 'wb') as f:
    #             # print(pickle.load(f))
    #             pickle.dump(response.text, f)
    #     with open('movie_data', 'rb') as f:
    #         print(pickle.load(f))
