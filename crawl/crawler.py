from bs4 import BeautifulSoup, Tag
import requests

from proxy_DB.my_client import RedisClient

INTI_PAGE = 15

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        """
        元编程
        用来新建一个crawl函数列表,实现批量调用
        :param name:
        :param bases:
        :param attrs:
        :return:
        """
        count = 0
        CrawFunc_list = []
        for k, v in attrs.items():
            if "crawl_" in k:
                CrawFunc_list.append(k)
                count += 1
        attrs['__CrawFunc__'] = CrawFunc_list
        attrs['__CrawFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def __init__(self):
        self.BD = RedisClient()

    def get_proxies(self, callback):
        # crawler每个ip网站的爬虫,由不同函数写成
        # 来调用自己的函数
        proxies = []
        for proxy in eval("self.{}()".format(callback)):  # 使用eval来执行代码
            print("获取代理:{}".format(proxy))
            proxies.append(proxy)

        return proxies

    def crawl_ip66(self, page_count=INTI_PAGE):
        """
        以crawl_开头 方便扩展,返回可迭代对象
        www.66ip.cn
        :param page_count:
        :return:
        """
        start_url = "http://www.66ip.cn/{}.html"
        urls = (start_url.format(i) for i in range(1, page_count + 1))
        for url in urls:
            print("抓取ing:{}".format(url))
            try:
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "lxml")
                trs = soup.find_all("tr")
                for tr in trs[2:]:
                    tds = list(tr.strings)  # type:list[Tag]
                    yield "{}:{}".format(*tds[0:2])
            except Exception as e:
                pass

    def crawl_xicidaili(self, page_count=INTI_PAGE):
        """
        http://www.xicidaili.com/
        :return:
        """
        start_url = "http://www.xicidaili.com/wt/{}"
        proxy_port = self.BD.random()
        proxy = {"http": "http://" + proxy_port}
        urls = (start_url.format(i) for i in range(1, page_count + 1))
        for url in urls:
            print("抓取ing:{}".format(url))
            try:
                #通过代理来获取ip,不然速度很慢
                res = requests.get(url, headers=header, proxies=proxy)
                soup = BeautifulSoup(res.text, "lxml")
                trs = soup.find_all("tr")
                for tr in trs[2:]:
                    tds = tr.find_all("td")  # type:list[Tag]
                    host, port = tds[1].string, tds[2].string
                    yield "{}:{}".format(host, port)
            except Exception as e:
                pass
