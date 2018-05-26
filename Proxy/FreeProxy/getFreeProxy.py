import re
import sys
import requests
import time
sys.path.append('../')
from webRequest.webRequest import WebRequest
from utilFunction import getHtmlTree
class GetFreeProxy(object):
    def __init__(self):
        pass



    @staticmethod
    def getProxyMethods():
        # return [ 'gbjProxy',  'fastProxy', 'cloudProxy', 'seaProxy']
        return {
            # 'gbjProxy': 'http://www.goubanjia.com/',
            # 'fastProxy': ' https://www.kuaidaili.com',
            # 'cloudProxy': 'http://www.ip3366.net/free/',
            # 'seaProxy': 'http://www.iphai.com/free/ng',
            # 'sixProxy': 'http://www.66ip.cn/',
            # 'mimiProxy': 'http://www.mimiip.com',
            'moguProxy': 'http://mogumiao.com'
        }

    @staticmethod
    def moguProxy():
        # a = {
        #         "code": "0",
        #          "msg":
        #              [
        #                 {"port": "37554", "ip": "218.73.128.104"},
        #                 {"port": "35591", "ip": "115.215.48.233"},
        #                 {"port": "20051", "ip": "218.66.146.184"},
        #                 {"port": "30917", "ip": "115.215.56.150"},
        #                 {"port": "28380", "ip": "117.69.97.134"}]
        #     }
        url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=95ef4dfabce94e5989bb0c633602d3e6&count=10&expiryDate=0&format=1&newLine=2'
        data = requests.get(url=url).json()
        while True:
            if(data['code']=='3001'):
                time.sleep(1)
                data = requests.get(url=url).json()
            break
        data = data['msg']
        for item in data:
            proxy = item['ip']+':'+item['port']
            yield proxy

    @staticmethod
    def wuyouProxy(page=10):
        """
        无忧代理 http://www.data5u.com/
        几乎没有能用的
        :param page: 页数
        :return:
        """
        url_list = [
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gngn/index.shtml',
        ]
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)

    # ok
    @staticmethod
    def sixProxy(area = 33, page=1):
        '''
        代理66 http://www.66ip.cn/
        高匿
        :param area: 抓取代理页数，page=1北京代理页，page=2上海代理页......
        :param page: 翻页
        :return:
        '''
        if area>33:
            area = 33
        for area_index in range(1, area + 1):
            for i in range(1, page + 1):
                url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                html_tree = getHtmlTree(url)
                tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                if len(tr_list) == 0:
                    continue
                for tr in tr_list:
                    yield tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0]
                break

    # em
    @staticmethod
    def manongProxy():
        """
        部分透明

        码农代理 https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=1']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall('data-ip="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})".+?>(\d+)</td>', r.text)
            for proxy in proxies:
                # print(proxy)
                yield ':'.join(proxy)

    # no
    @staticmethod
    def xiciProxy(page_count=2):
        """
        透明的，不想用

        西刺代理 http://www.xicidaili.com
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    # ok
    @staticmethod
    def gbjProxy():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                            and not(contains(@style, 'display:none'))
                                            and not(contains(@class, 'port'))
                                            ]/text()
                                    """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                yield '{}:{}'.format(ip_addr, port)
            except Exception as e:
                pass

    # ok
    @staticmethod
    def fastProxy():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/'
        ]
        for url in url_list:
            for page in range(1, 5):
                page_url = url.format(page=page)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])

    # no
    @staticmethod
    def mimiProxy():
        """
        秘密代理 http://www.mimiip.com
        估计没啥可用的，暂时不用了
        """
        url_gngao = ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)]  # 国内高匿
        # url_gnpu = ['http://www.mimiip.com/gnpu/%s' % n for n in range(1, 10)]  # 国内普匿
        # url_gntou = ['http://www.mimiip.com/gntou/%s' % n for n in range(1, 10)]  # 国内透明
        url_gw = ['http://www.mimiip.com/hw/%s' % n for n in range(1, 10)]  #国外
        url_list = url_gngao + url_gw

        request = WebRequest()
        for url in url_list:
            r = request.get(url, use_proxy=True)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W].*<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    # ok
    @staticmethod
    def cloudProxy():
        """
        云代理
        高匿
        :return:
        """
        urls = ['http://www.ip3366.net/free/']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    # ok
    @staticmethod
    def seaProxy():
        """
        IP海 http://www.iphai.com/free/ng
        高匿
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            # 'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            # 'http://www.iphai.com/free/wp'
        ]
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    # em
    @staticmethod
    def fwallProxy():
        """
        墙外网站 cn-proxy
        不确定是否匿名
        :return:
        """
        urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    # em
    @staticmethod
    def swallProxy():
        """
        部分匿名
        https://proxy-list.org/english/index.php
        :return:
        """
        urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
        request = WebRequest()
        import base64
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
            for proxy in proxies:
                yield base64.b64decode(proxy).decode()

    # em
    @staticmethod
    def twallProxy():
        urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
        request = WebRequest()
        for url in urls:
            r = request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


if __name__ == '__main__':
    getfree = GetFreeProxy()
    getfree.moguProxy()
    # url = 'https://indienova.com/steam/mustbuy'
    # headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}
    # pp = GetFreeProxy()
    # for i in pp.wuyouProxy():
    #     proxies = {
    #         'http':i
    #     }
    #     print(i)
    #     print(requests.get(url=url, headers=headers, proxies=proxies).status_code)


