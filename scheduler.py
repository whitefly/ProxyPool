import time
from crawl.getter import Getter
from crawl.proxy_test import Tester
from proxy_api import app
from multiprocessing import Process

TESTER_ENABLED = True
CRAWLER_ENABLED = True
API_ENABLED = True

TESTER_CYCLE = 60
CRAWLER_CYCLE = 120


class Scheduler():
    def run_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print("测试模块:开始运行")
            tester.run()
            time.sleep(cycle)

    def run_crawler(self, cycle=CRAWLER_CYCLE):
        getter = Getter()
        while True:
            print("爬取模块:开始运行")
            getter.run()
            time.sleep(cycle)

    def run_flask(self):
        print("api模块:开始运行")
        app.run()

    def run(self):
        # 开3个进程,不断运行
        if TESTER_ENABLED:
            test_process = Process(target=self.run_tester)
            test_process.start()

        if CRAWLER_ENABLED:
            crawler_process = Process(target=self.run_crawler)
            crawler_process.start()

        if API_ENABLED:
            flask_process = Process(target=self.run_flask)
            flask_process.start()


if __name__ == '__main__':
    S = Scheduler()
    S.run()
