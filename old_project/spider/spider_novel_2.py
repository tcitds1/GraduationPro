from bs4 import BeautifulSoup
from urllib import request
"""
1.获取小说每个章节的url链接
2.爬取每章链接的内容
"""
if __name__ == '__main__':
    chapter_url = 'http://www.biqukan.com/1_1094/'
    user_headers = {}
    user_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    req = request.Request(url=chapter_url,headers=user_headers)
    html = request.urlopen(req).read().decode('gbk','ignore')

    bs_chapter = BeautifulSoup(html,'lxml')

    listmain = bs_chapter.find(class_="listmain")
    download_soup = BeautifulSoup(str(listmain),'lxml')
    index_zero = False
    for dd in download_soup.dl.children:
        if dd.string !='\n':
            if dd.string== '《一念永恒》正文卷':
                    index_zero = True
            if index_zero==True and dd.a!=None:
                chapter_number = dd.string
                download_url = "http://www.biqukan.com/1_1094/" + dd.a.get('href')
                print(chapter_number + download_url)
