from flask import Flask, g

from proxy_DB.my_client import RedisClient

_all_ = ["app"]
app = Flask(__name__)


def get_con():
    if not hasattr(g, "redis"):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def home():
    return "这里是一个获取有效代理的api网站"


@app.route('/random')
def get_proxy():
    con = get_con()
    return con.random()


@app.route('/count')
def get_count():
    con = get_con()
    return str(con.get_count())


if __name__ == '__main__':
    app.run()
