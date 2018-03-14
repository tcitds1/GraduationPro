from bs4 import BeautifulSoup
from urllib import request
if __name__ == '__main__':
    url = 'http://www.biqukan.com/1_1094/5403177.html'
    req = request.Request(url)
    response = request.urlopen(req)
    html = response.read().decode('gbk','ignore')

    bs = BeautifulSoup(html,'lxml')
    texts = bs.find_all(id="content")
    soup_text = BeautifulSoup(str(texts), 'lxml')
    print(soup_text.div.text.replace('\xa0',''))

# -*- coding:UTF-8 -*-
# from urllib import request
# from bs4 import BeautifulSoup
#
# if __name__ == "__main__":
#     download_url = 'http://www.biqukan.com/1_1094/5403177.html'
#     head = {}
#     head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
#     download_req = request.Request(url = download_url, headers = head)
#     download_response = request.urlopen(download_req)
#     download_html = download_response.read().decode('gbk','ignore')
#     soup_texts = BeautifulSoup(download_html, 'lxml')
#     soup_text = BeautifulSoup(str(texts), 'lxml')
#     #将\xa0无法解码的字符删除
#     print(soup_text.div.text.replace('\xa0',''))