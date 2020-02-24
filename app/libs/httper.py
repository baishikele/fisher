import urllib
# 系统库不好用，url带汉字的要转码，response要把字节码转str，还要处理404异常

# 爬虫：
# scrapy处理多线程并发。requests+beatiful soap 比较精简
import requests


# python2 是否写继承object不一样
class HTTP(object):
    # 代码封装
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else 'http_response:这是一个空字符串'
        return r.json() if return_json else r.text