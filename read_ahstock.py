#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/10/21 20:21 
# @Author : yangpingyan@gmail.com
import re
import urllib
import pandas as pd
import random


class ReadStockAH():
    # AH股关联代码：http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/var%20hk_corrastock=/HK_CorrStock.getCorrstock
    ahstock_dict = {'hk00042': 'sz000585', 'hk00168': 'sh600600', 'hk00177': 'sh600377', 'hk00187': 'sh600860',
                    'hk00317': 'sh600685', 'hk00323': 'sh600808', 'hk00338': 'sh600688', 'hk00347': 'sz000898',
                    'hk00358': 'sh600362', 'hk00386': 'sh600028', 'hk00525': 'sh601333', 'hk00548': 'sh600548',
                    'hk00553': 'sh600775', 'hk00588': 'sh601588', 'hk00670': 'sh600115', 'hk00719': 'sz000756',
                    'hk00753': 'sh601111', 'hk00763': 'sz000063', 'hk00874': 'sh600332', 'hk00902': 'sh600011',
                    'hk00914': 'sh600585', 'hk00921': 'sz000921', 'hk00991': 'sh601991', 'hk00995': 'sh600012',
                    'hk00998': 'sh601998', 'hk01033': 'sh600871', 'hk01053': 'sh601005', 'hk01055': 'sh600029',
                    'hk01065': 'sh600874', 'hk01071': 'sh600027', 'hk01072': 'sh600875', 'hk01108': 'sh600876',
                    'hk01138': 'sh600026', 'hk01171': 'sh600188', 'hk01398': 'sh601398', 'hk02318': 'sh601318',
                    'hk02338': 'sz000338', 'hk02600': 'sh601600', 'hk02628': 'sh601628', 'hk03328': 'sh601328',
                    'hk03988': 'sh601988', 'hk03968': 'sh600036', 'hk00939': 'sh601939', 'hk01088': 'sh601088',
                    'hk01919': 'sh601919', 'hk02883': 'sh601808', 'hk00857': 'sh601857', 'hk00390': 'sh601390',
                    'hk01898': 'sh601898', 'hk01186': 'sh601186', 'hk02899': 'sh601899', 'hk01812': 'sz000488',
                    'hk01766': 'sh601766', 'hk02866': 'sh601866', 'hk02727': 'sh601727', 'hk01988': 'sh600016',
                    'hk02601': 'sh601601', 'hk01618': 'sh601618', 'hk00107': 'sh601107', 'hk01288': 'sh601288',
                    'hk00568': 'sz002490', 'hk02880': 'sh601880', 'hk02208': 'sz002202', 'hk01157': 'sz000157',
                    'hk02009': 'sh601992', 'hk02607': 'sh601607', 'hk01211': 'sz002594', 'hk02333': 'sh601633',
                    'hk06030': 'sh600030', 'hk01336': 'sh601336', 'hk01800': 'sh601800', 'hk02238': 'sh601238',
                    'hk06837': 'sh600837', 'hk00895': 'sz002672', 'hk00038': 'sh601038', 'hk03993': 'sh603993',
                    'hk01057': 'sz002703', 'hk00564': 'sh601717', 'hk02039': 'sz000039', 'hk02196': 'sh600196',
                    'hk06818': 'sh601818', 'hk01513': 'sz000513', 'hk02202': 'sz000002', 'hk01776': 'sz000776',
                    'hk03606': 'sh600660', 'hk06886': 'sh601688', 'hk03958': 'sh600958', 'hk00811': 'sh601811',
                    'hk06178': 'sh601788', 'hk01635': 'sh600635', 'hk01375': 'sh601375', 'hk06881': 'sh601881',
                    'hk03369': 'sh601326', 'hk06099': 'sh600999', 'hk06116': 'sh603157', 'hk01533': 'sz002910',
                    'hk02611': 'sh601211', 'hk01528': 'sh601828', 'hk01330': 'sh601330', 'hk06066': 'sh601066',
                    'hk06869': 'sh601869', 'hk02068': 'sh601068', 'hk06196': 'sz002936', 'hk01787': 'sh600547',
                    'hk01772': 'sz002460'}
    astock_df = pd.DataFrame(
        index=['acode', 'name', 'open', 'close', 'aprice', 'high', 'low', 'buy', 'sell', 'turnover', 'volume',
               'bid1_volume', 'bid1', 'bid2_volume', 'bid2', 'bid3_volume', 'bid3', 'bid4_volume', 'bid4',
               'bid5_volume', 'bid5', 'ask1_volume', 'ask1', 'ask2_volume', 'ask2', 'ask3_volume', 'ask3',
               'ask4_volume', 'ask4', 'ask5_volume', 'ask5', 'date', 'time'])
    hstock_df = pd.DataFrame(
        index=['hcode', 'ename', 'cname', 'unknow1', 'unknow2', 'unknow3', 'unknow4', 'hprice', 'unknow6', 'unknow7',
               'unknow8', 'unknow9', 'unknow10', 'unknow11', 'unknow12', 'unknow13', 'unknow14', 'unknow15', ])
    ahstocks_df = pd.DataFrame.from_dict(ahstock_dict, orient='index', columns=['acode'])
    ahstocks_df['hcode'] = ahstocks_df.index

    def __init__(self):
        pass

    @property
    def stock_api(self):
        return "http://hq.sinajs.cn/rn={}&list=".format(self._random())

    @property
    def grep_str_astock(self):
        return re.compile(r"([szh\d]+)=.([^\s][^,]+?)%s%s" % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2))

    @property
    def grep_str_hstock(self):
        return re.compile(r"(hk\d+)=.([\w ]+),([^\s][^,]+?)%s" % (r",([-\d.]+)" * 15))

    @property
    def grep_str_hkdcny(self):
        return re.compile(r"(\w+)=\"([\d:]+)%s,([\S]+),([\d-]+)" % (r",([\.\d]+)" * 8))

    @staticmethod
    def _random(length=13):
        start = 10 ** (length - 1)
        end = (10 ** length) - 1
        return str(random.randint(start, end))

    def read_stock_data(self, code_list, grep_str, df):
        code = ",".join(code_list)
        url = self.stock_api + code
        response = urllib.request.urlopen(url)
        rep_data = response.read().decode("gbk")
        stocks_detail = "".join(rep_data)
        result = grep_str.finditer(stocks_detail)
        for stock_match_object in result:
            stock = stock_match_object.groups()
            df[stock[0]] = stock

        df = df.T
        print(df)
        return df

    def get_ahrate(self):
        # 获取A股价格
        df = self.read_stock_data(self.ahstocks_df['acode'].values.tolist(), self.grep_str_astock, self.astock_df)
        df = df[['acode', 'name', 'aprice']]
        self.ahstocks_df = pd.merge(self.ahstocks_df, df, on='acode')
        # 获取H股价格
        df = self.read_stock_data(self.ahstocks_df['hcode'].values.tolist(), self.grep_str_hstock, self.hstock_df)
        df = df[['hcode', 'hprice']]
        self.ahstocks_df = pd.merge(self.ahstocks_df, df, on='hcode')
        # 获取港币对人民币汇率
        df = pd.DataFrame()
        df = self.read_stock_data(['HKDCNY'], self.grep_str_hkdcny, df)
        hkdcny = float(df.iat[0, 2])
        # 计算AH股比价
        self.ahstocks_df['aprice'] = self.ahstocks_df['aprice'].astype(float)
        self.ahstocks_df['hprice'] = self.ahstocks_df['hprice'].astype(float)
        self.ahstocks_df['ahrate'] = self.ahstocks_df['hprice'] / self.ahstocks_df['aprice'] * hkdcny

        return self.ahstocks_df

    def get_buylist(self):
        df = self.get_ahrate()
        df.sort_values(by='ahrate', ascending=False, inplace=True)
        buylist = df[df['ahrate']>1.0]['acode'].tolist()

        return buylist


# In[]


