import requests
import re
from bs4 import BeautifulSoup
import os
import time
import random
import lxml
from lxml import html
etree = html.etree
key = input('please enter key you want to download')
class Spider():
    def __init__(self):
        self.path = '/Users/justin_lee/Desktop/spiderimg'
        self.url = 'https://alpha.wallhaven.cc/search?q={}&search_image='.format(key)
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3393.4 Safari/537.36'}
    def create_path(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    def get_totalNums(self):
        rs = requests.get(self.url, headers = self.headers)
        bs = BeautifulSoup(rs.text,"lxml")
        # print(bs.prettify())
        # if(rs.status_code == 200):
        #     bs = BeautifulSoup(rs.text)
            # print(bs.prettify())
        headers = bs.find_all(attrs={'class': 'listing-header'})
        header = BeautifulSoup(str(headers), "lxml")
        h1 = header.h1
        strings = h1.get_text()
        total_numbers = int(re.sub('\D', '', strings))
        return total_numbers
    def get_imgid(self, number):
        # total_numbers =  self.get_totalNums()
        # pages = int(total_numbers/24 + 1)
        url = 'https://alpha.wallhaven.cc/search?q={}&search_image=&page={}'.format(key, number)
        rs = requests.get(url,headers = self.headers)
        bs = BeautifulSoup(rs.text, "lxml")
        a_tags = bs.find_all("a", class_ = "jsAnchor thumb-tags-toggle tagged")
        imglist = []
        for a_tag in a_tags:
            href = a_tag['href']
            imgid = re.sub('\D','',href)
            imglist.append(imgid)
        return imglist
    def downlod_img(self, imgid, count):
        # html = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + string + '.jpg'
        img_url1 = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + imgid + '.jpg'
        img_url2 = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + imgid + '.png'
        rs = requests.get(img_url1, headers = self.headers)
        # imgpath = ''
        imgpath = '/Users/justin_lee/Desktop/spiderimg/' + key + str(count) + '.jpg'
        if(rs.status_code == 404):
            rs = requests.get(img_url2, headers = self.headers)
            if(rs.status_code == 404):
                return
            imgpath = '/Users/justin_lee/Desktop/spiderimg/' +  key + str(count) + '.png'
        with open(imgpath, 'wb+') as stream:
            stream.write(rs.content)
            print('the {} img {} has been download'.format(key,count))
        time.sleep(random.uniform(0, 1))
    def main_function(self):
        self.create_path()
        total_num = self.get_totalNums()
        pages = int(total_num/24 + 1)
        j = 1
        for page in range(pages):
            imglist = self.get_imgid(page)
            for imgid in imglist:
                self.downlod_img(imgid, j)
                j += 1
if __name__ == '__main__':
    spider = Spider()
    spider.main_function()
    # spider = Spider()
    # spider.get_totalNums()
    # headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3393.4 Safari/537.36'}
    # url = 'https://alpha.wallhaven.cc/search?q=cat&search_image='
    # rs = requests.get(url,headers = headers)
    # bs = BeautifulSoup(rs.text, "lxml")
    # # print(bs.prettify())
    # headers = bs.find_all(attrs = {'class':'listing-header'})
    # header = BeautifulSoup(str(headers), "lxml")
    # h1 = header.h1
    # strings = h1.get_text()
    # total_numbers = int(re.sub('\D','',strings))
    # print(total_numbers)
    # h1.i.extract()
    # h1.span.extract()
    # spider = Spider()
    # spider.get_totalNums()
    # url = 'https://alpha.wallhaven.cc/search?q=sky&search_image=&page=1'
    # rs = requests.get(url, headers = headers)
    # bs = BeautifulSoup(rs.text, "lxml")
    # a_tags = bs.find_all("a", class_="jsAnchor thumb-tags-toggle tagged")
    # imglist = []
    # for a_tag in a_tags:
    #     href = a_tag['href']
    #     imgid = re.sub('\D', '', href)
    #     imglist.append(imgid)
    # print(imglist)
    # url = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-637218.png'
    # rs = requests.get(url, headers = headers)
    # print(rs.status_code)