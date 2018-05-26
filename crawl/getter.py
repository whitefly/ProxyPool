from crawl.crawler import Crawler
from proxy_DB.my_client import RedisClient

POOL_MAX_COUNT = 10000


class Getter():
    def __init__(self):
        self.crawler = Crawler()
        self.redis = RedisClient()

    def is_over_limet(self):
        return self.redis.get_count() > POOL_MAX_COUNT

    def run(self):
        if not self.is_over_limet():
            for crawFunc_label in self.crawler.__CrawFunc__:
                proxies = self.crawler.get_proxies(crawFunc_label)
                for proxy in proxies:
                    if not self.redis.exist(proxy):
                        self.redis.add(proxy)


if __name__ == '__main__':
    # 测试
    g = Getter()
    g.run()
