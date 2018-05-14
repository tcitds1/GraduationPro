# from urllib import request
# if __name__ == '__main__':
# 	url = 'http://www.whatismyip.com.tw/'
# 	proxy = {'http':'219.138.58.11'}
# 	#create proxyHeadle
# 	proxy_handle = request.ProxyHandler(proxy)
# 	#build openner
# 	openner = request.build_opener(proxy_handle)
# 	openner.addheaders = [('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36')]
# 	#install openner
# 	request.install_opener(openner)
# 	#send request
# 	response = request.urlopen(url)
# 	print(response.read().decode('utf-8'))

# -*- coding: UTF-8 -*-
from urllib import request

if __name__ == "__main__":
    #访问网址
    url = 'http://www.whatismyip.com.tw/'
    #这是代理IP
    proxy = {'http':'110.73.3.68'}
    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    #使用自己安装好的Opener
    response = request.urlopen(url)
    #读取相应信息并解码
    html = response.read().decode("utf-8")
    #打印信息
    print(html)