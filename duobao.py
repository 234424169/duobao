"""
用于夺宝岛自动抢商品
下面的ITEMID为商品ID，在URL上能看到，自行修改
MAX_PRICE为你能出的预期最高价，超过了不会拍
LIMIT_VALUE为离结束多少秒进行拍价，太短了容易超时，太长了会被人超过，这个自己权衡下。
COOKIE是你个人的登录信息，在页面登录夺宝岛后，按F12出现浏览器调试模式，随便找一个请求，把请求的COOKIE拷贝下来
"""
import json
import time
import requests


JSONP_BEGIN = r'try{callback('
JSONP_END = r')}catch(e){};'

ITEMID = '17304865'
MAX_PRICE = 32
LITMIT_VALUE = 1.5
COOKIE = '填上自己的COOKIE信息'
HEADER = {'Referer': 'http://dbditem.jd.com', 'Cookie':COOKIE}

def from_jsonp(jsonp_str):
    """
    用于解析jsonp
    """
    jsonp_str = jsonp_str.strip()
    if not jsonp_str.startswith(JSONP_BEGIN) or \
            not jsonp_str.endswith(JSONP_END):
        raise ValueError('Invalid JSONP')
    return json.loads(jsonp_str[len(JSONP_BEGIN):-len(JSONP_END)])

def bid(bid_itemid, bid_price):
    """
    下单
    """
    url = 'http://dbditem.jd.com/services/bid.action?paimaiId=' + bid_itemid + '&price=' + \
    str(bid_price) + '&proxyFlag=0&bidSource=0'
    response = requests.get(url, headers=HEADER)
    print(response.text)

def query(query_itemid):
    """
    查询价格和时间
    """
    url = 'http://bid.jd.com/json/current/englishquery?skuId=0&start=0&end=9&paimaiId=' + \
    query_itemid
    raw_result = requests.get(url, headers=HEADER)
    response = from_jsonp(raw_result.text)
    return response

def run():
    """
    主函数
    """
    result = query(ITEMID)

    remain_time = result['remainTime']
    bid_time = int(remain_time)/1000 - LITMIT_VALUE
    print('先睡眠等等' + str(bid_time) + '秒')
    time.sleep(bid_time)

    print('起床了')
    result = query(ITEMID)
    price = int(result['currentPrice'])
    print('目前价格为' + str(price))
    if price + 1 <= MAX_PRICE:
        bid(ITEMID, price + 1)
    else:
        print('超过了预期价格')

if __name__ == '__main__':
    run()
