import requests
from lxml import html
etree = html.etree

url = 'https://movie.douban.com/'
headers = {}
headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
rs = requests.get(url = url, headers = headers)
html = etree.HTML(rs.text)
texts = html.xpath('//a/text()')
print(texts)