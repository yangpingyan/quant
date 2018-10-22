#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/10/21 20:21 
# @Author : yangpingyan@gmail.com
#!/usr/bin/env python
# coding: utf-8
# @Time : 2018/10/22 15:58
# @Author : yangpingyan@gmail.com

import random
import re

import abc
import json
import multiprocessing.pool
import warnings

import easyutils
import requests
import os

STOCK_CODE_PATH = "stock_codes.conf"


def update_stock_codes():
    """获取所有股票 ID 到 all_stock_code 目录下"""
    all_stock_codes_url = "http://www.shdjt.com/js/lib/astock.js"
    grep_stock_codes = re.compile(r"~(\d+)`")
    response = requests.get(all_stock_codes_url)
    all_stock_codes = grep_stock_codes.findall(response.text)
    with open(stock_code_path(), "w") as f:
        f.write(json.dumps(dict(stock=all_stock_codes)))


def get_stock_codes(realtime=False):
    """获取所有股票 ID 到 all_stock_code 目录下"""
    if realtime:
        all_stock_codes_url = "http://www.shdjt.com/js/lib/astock.js"
        grep_stock_codes = re.compile(r"~(\d+)`")
        response = requests.get(all_stock_codes_url)
        stock_codes = grep_stock_codes.findall(response.text)
        with open(stock_code_path(), "w") as f:
            f.write(json.dumps(dict(stock=stock_codes)))
        return stock_codes

    with open(stock_code_path()) as f:
        return json.load(f)["stock"]


def stock_code_path():
    return os.path.join(os.path.dirname(__file__), STOCK_CODE_PATH)

class BaseQuotation(metaclass=abc.ABCMeta):
    """行情获取基类"""

    max_num = 800  # 每次请求的最大股票数

    @property
    @abc.abstractmethod
    def stock_api(self) -> str:
        """
        行情 api 地址
        """
        pass

    def __init__(self):
        self._session = requests.session()
        stock_codes = self.load_stock_codes()
        self.stock_list = self.gen_stock_list(stock_codes)

    def gen_stock_list(self, stock_codes):
        stock_with_exchange_list = self._gen_stock_prefix(stock_codes)

        if self.max_num > len(stock_with_exchange_list):
            request_list = ",".join(stock_with_exchange_list)
            return [request_list]

        stock_list = []
        request_num = len(stock_codes) // (self.max_num + 1) + 1
        for range_start in range(request_num):
            num_start = self.max_num * range_start
            num_end = self.max_num * (range_start + 1)
            request_list = ",".join(
                stock_with_exchange_list[num_start:num_end]
            )
            stock_list.append(request_list)
        return stock_list

    def _gen_stock_prefix(self, stock_codes):
        return [
            easyutils.stock.get_stock_type(code) + code[-6:]
            for code in stock_codes
        ]

    @staticmethod
    def load_stock_codes():
        with open(stock_code_path()) as f:
            return json.load(f)["stock"]

    @property
    def all(self):
        warnings.warn("use market_snapshot instead", DeprecationWarning)
        return self.get_stock_data(self.stock_list)

    @property
    def all_market(self):
        """return quotation with stock_code prefix key"""
        return self.get_stock_data(self.stock_list, prefix=True)

    def stocks(self, stock_codes, prefix=False):
        return self.real(stock_codes, prefix)

    def real(self, stock_codes, prefix=False):
        """return specific stocks real quotation
        :param stock_codes: stock code or list of stock code,
                when prefix is True, stock code must start with sh/sz
        :param prefix: if prefix i True, stock_codes must contain sh/sz market
            flag. If prefix is False, index quotation can't return
        :return quotation dict, key is stock_code, value is real quotation.
            If prefix with True, key start with sh/sz market flag

        """
        if not isinstance(stock_codes, list):
            stock_codes = [stock_codes]

        stock_list = self.gen_stock_list(stock_codes)
        return self.get_stock_data(stock_list, prefix=prefix)

    def market_snapshot(self, prefix=False):
        """return all market quotation snapshot
        :param prefix: if prefix is True, return quotation dict's  stock_code
             key start with sh/sz market flag
        """
        return self.get_stock_data(self.stock_list, prefix=prefix)

    def get_stocks_by_range(self, params):
        headers = {
            "Accept-Encoding": "gzip, deflate, sdch",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/54.0.2840.100 "
                "Safari/537.36"
            ),
        }

        r = self._session.get(self.stock_api + params, headers=headers)
        return r.text

    def get_stock_data(self, stock_list, **kwargs):
        """获取并格式化股票信息"""
        res = self._fetch_stock_data(stock_list)
        return self.format_response_data(res, **kwargs)

    def _fetch_stock_data(self, stock_list):
        """获取股票信息"""
        pool = multiprocessing.pool.ThreadPool(len(stock_list))
        try:
            res = pool.map(self.get_stocks_by_range, stock_list)
        finally:
            pool.close()
        return [d for d in res if d is not None]

    def format_response_data(self, rep_data, **kwargs):
        pass



class Sina(BaseQuotation):
    """新浪免费行情获取"""

    max_num = 800
    grep_detail = re.compile(
        r"(\d+)=([^\s][^,]+?)%s%s" % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    )
    grep_detail_with_prefix = re.compile(
        r"(\w{2}\d+)=([^\s][^,]+?)%s%s"
        % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    )

    @property
    def stock_api(self) -> str:
        return f"http://hq.sinajs.cn/rn={self._random()}&list="

    @staticmethod
    def _random(length=13) -> str:
        start = 10 ** (length - 1)
        end = (10 ** length) - 1
        return str(random.randint(start, end))
#  r"(\d+)=([^\s][^,]+?)%s%s" % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2)
    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = "".join(rep_data)
        grep_str = self.grep_detail_with_prefix if prefix else self.grep_detail
        result = grep_str.finditer(stocks_detail)
        all = grep_str.findall(stocks_detail)
        stock_dict = dict()
        for stock_match_object in result:
            stock = stock_match_object.groups()
            stock_dict[stock[0]] = dict(
                name=stock[1],
                open=float(stock[2]),
                close=float(stock[3]),
                now=float(stock[4]),
                high=float(stock[5]),
                low=float(stock[6]),
                buy=float(stock[7]),
                sell=float(stock[8]),
                turnover=int(stock[9]),
                volume=float(stock[10]),
                bid1_volume=int(stock[11]),
                bid1=float(stock[12]),
                bid2_volume=int(stock[13]),
                bid2=float(stock[14]),
                bid3_volume=int(stock[15]),
                bid3=float(stock[16]),
                bid4_volume=int(stock[17]),
                bid4=float(stock[18]),
                bid5_volume=int(stock[19]),
                bid5=float(stock[20]),
                ask1_volume=int(stock[21]),
                ask1=float(stock[22]),
                ask2_volume=int(stock[23]),
                ask2=float(stock[24]),
                ask3_volume=int(stock[25]),
                ask3=float(stock[26]),
                ask4_volume=int(stock[27]),
                ask4=float(stock[28]),
                ask5_volume=int(stock[29]),
                ask5=float(stock[30]),
                date=stock[31],
                time=stock[32],
            )
        return stock_dict

quotation = Sina()
test = quotation.stocks(['000001', '162411'])
print(test)



url_pre = 'http://hq.sinajs.cn/rn=&list='
code = 'rt_hkhqtime,s_sh000001,s_sz399001,rt_hkHSI,rt_hkHSCEI,HKDCNY,s_sh000905,s_sh000300,sh601318,sz000001'
url = url_pre + code

hk_corrastock

response = urllib.request.urlopen(url)
html = response.read().decode("gbk")
soup = BeautifulSoup(html)
print(soup.prettify())
/ html / body / div[3]
body > div.i_bd.w95.i_clear.i_allbg
div = soup.find_all(class_='i_bd w95 i_clear i_allbg')
div
a_bf = BeautifulSoup(str(div[0]))
a = a_bf.find_all('a')
for each in a:
    print(each.string, each.get('href'))
    break

scrapy
startproject
tutorial

scrapy
shell
http: // finance.sina.com.cn / stock / hkstock / anh.shtml
response.xpath(r'//*[@id="table_container"]').extract()
