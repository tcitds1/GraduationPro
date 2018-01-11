from urllib import request
from urllib import error
url = "http://www.yiwenxiang.com/"
req = request.Request(url)
try:
	response = request.urlopen(req)
	html = response.read()
	print(html)
except error.URLError as e:
	print(e.reason)
except:
	print('未知错误')