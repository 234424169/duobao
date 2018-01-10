"""
用于拍拍二手（旧版夺宝岛）自动抢商品
下面的ITEMID为商品ID，在URL上能看到，自行修改
MAX_PRICE为你能出的预期最高价，超过了不会拍
LIMIT_VALUE为离结束多少秒进行拍价，可以为负数，因为每个人的时间跟服务器有差异，需要自己调整，默认是0。
COOKIE是你个人的登录信息，在页面登录夺宝岛后，按F12出现浏览器调试模式，随便找一个请求，把请求的COOKIE拷贝下来
"""
import time
import requests
from bs4 import BeautifulSoup

ITEMID = '112567091'
MAX_PRICE = 1  #元为单位
LITMIT_VALUE = 0 #秒为单位
COOKIE = '你自己的cookie'
HEADER = {'Cookie':COOKIE}


def bid(bid_itemid, bid_price):
    """
    下单
    """
    url = 'https://used-api.jd.com/auctionRecord/offerPrice?auctionId=' + bid_itemid + '&price=' + \
    str(bid_price)
    response = requests.get(url, headers=HEADER)
    print(response.text)

def query(query_itemid):
    """
    查询价格和剩余时间
    """
    url = 'http://paipai.jd.com/auction/detail?auctionId=' + \
    query_itemid
    raw_result = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(raw_result.text, "html.parser")
    #解析返回结果
    script_text = soup('script')[0].text
    #print(script_text)
    end_time_text = 'endTime: new Date('
    current_time_text = 'currentTime: new Date('
    end_time_index = script_text.find(end_time_text, 0)
    current_time_index = script_text.find(current_time_text, 0)
    end_time = script_text[end_time_index+len(end_time_text):end_time_index+len(end_time_text)+13]
    current_time = script_text[current_time_index+len(current_time_text):current_time_index+len(current_time_text)+13]
    remain = int(end_time) - int(current_time)

    #获取价格
    price_text = 'currentPrice:'
    price_begin_index = script_text.find(price_text, 0)
    price_end_index = script_text.find('\n', price_begin_index)
    price = script_text[price_begin_index+len(price_text):price_end_index]
    return remain, float(price)

def run():
    """
    主函数
    """
    remain_time, price = query(ITEMID)
    bid_time = int(remain_time)/1000 - LITMIT_VALUE
    if bid_time < 0:
        print('等待时间为负数')
        return 
    print('先睡眠等等' + str(bid_time) + '秒')
    time.sleep(bid_time)

    print('起床了')
    remain_time, price = query(ITEMID)
    #价格向下取整
    price = int(price)
    print('目前价格为' + str(price))
    if price + 1 <= MAX_PRICE:
        bid(ITEMID, price + 1)
    else:
        print('超过了预期价格')

if __name__ == '__main__':
    run()
