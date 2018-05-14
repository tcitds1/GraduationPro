#_*_ coding:utf-8 _*_
import requests
from PIL import  Image
def spiderhtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3386.1 Safari/537.36'
    }
    # 传递url参数
    # requests.get(url,params, **kwargs)
    # payload = {'key1': 'ywx', 'key2': '1997'}
    # requests.get(url,params=payload);
    response = requests.get(url)
    # print(response.text)
    print(response.encoding)
    # response.content 以字节方式访问响应体，对于非文本请求 多用于图像处理
    
spiderhtml('https://github.com/kennethreitz')



