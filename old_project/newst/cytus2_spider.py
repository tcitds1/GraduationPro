
import requests
from bs4 import BeautifulSoup
import os
class Spider:
    def __init__(self):
        self.url = 'https://wikiwiki.jp/cytus-2/%E6%A5%BD%E6%9B%B2%E4%B8%80%E8%A6%A7'
        headers = {}
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        headers['Host'] = 'wikiwiki.jp'
        headers['Connection'] = 'keep-alive'
        headers['Referer'] = 'https://wikiwiki.jp/cytus-2/'
        headers['Upgrade-Insecure-Requests'] = '1'
        #设置headers 后来发现访问403的问题不是header 虽然加headers可能没什么鸟用 但是还是先设着吧
        self.headers = headers
        #放图片的地址
        self.path = 'C:/Users/深海里的猫/Desktop/spiderimg/'
        #域名前缀
        self.before_url = 'https://wikiwiki.jp/'
        self.singer_name = ''
    def creat_path(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
    def download(self):
        rs = requests.get(url=self.url, headers=self.headers)
        bf = BeautifulSoup(rs.text, 'lxml')
        singers_array = bf.find_all('div', class_='ie5')
        i = 0;
        while i < len(singers_array)-1:
            if i == 0:
                self.singer_name = 'PAFF/'
            if i == 1:
                self.singer_name = 'NEKO#ΦωΦ/'
            if i == 2:
                self.singer_name = 'ROBO_Head/'
            if i == 3:
                self.singer_name = 'Xenon/'
            if i == 4:
                self.singer_name = 'ConneR/'
            if i == 5:
                self.singer_name = 'Cherry/'
            path = self.path +self.singer_name
            self.creat_path(path)

            a_tags = singers_array[i].find_all('a')

            for a_tag in a_tags:
                song_name = a_tag['title']
                song_links = self.before_url + a_tag['href']
                rs1 = requests.get(url = song_links, headers = self.headers)
                bf1 = BeautifulSoup(rs1.text, 'lxml')
                img_tag = bf1.find_all('img')[8]
                img_src_complete = self.before_url + img_tag['src']
                rs2 = requests.get(url = img_src_complete, headers = self.headers)
                img_path = self.path + self.singer_name + song_name + '.jpg'
                with open(img_path, 'wb+') as stream:
                    stream.write(rs2.content)
                print(song_name + ' img has downloaded')

            i = i+1

if __name__ == '__main__':
    spider = Spider()
    spider.download()