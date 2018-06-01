import requests
from pyquery import PyQuery


class login(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Host": "github.com"
        }
        self.login_url = "https://github.com/login"
        self.post_url = "https://github.com/session"
        self.logined_url = "https://github.com/settings/profile"
        self.session = requests.session()

    def get_token(self):
        data = self.session.get(self.login_url, headers=self.headers)
        if data.status_code == 200:
            doc = PyQuery(data.text)  # type:PyQuery
            token = doc('div#login form input[name=authenticity_token]').attr('value')
            return token
        else:
            return None

    def login(self, user, password):
        post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": self.get_token(),
            "login": user,
            "password": password
        }
        # 填入post提交信息
        resp = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if resp.status_code == 200:
            print("{}:登录成功".format(user))

        data = self.session.get(self.logined_url, headers=self.headers)
        if data.status_code == 200:
            self.get_profile(data.text)

    def get_profile(self, init_code):
        # 获取数据
        doc = PyQuery(init_code)
        blog = doc("input#user_profile_blog").attr("value")
        print("个人博客地址为:{}".format(blog))


if __name__ == '__main__':
    L = login()
    user = "316447676@qq.com"
    password = "xxx"

    L.login(user, password)
