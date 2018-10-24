#!/usr/bin/env python 
# coding: utf-8
# @Time : 2018/10/24 10:09 
# @Author : yangpingyan@gmail.com


import read_ahstock
import easytrader
import warnings
import tushare as ts
import pandas as pd
import time

pd.set_option('display.max_columns', 50)
# Suppress warnings
warnings.filterwarnings('ignore')
print("自动交易时请禁止屏幕缩放")
user = easytrader.use('ths')
user.connect(r'C:\同花顺软件\同花顺\xiadan.exe')

# 获取帐户信息
account = user.balance
position = user.position
for pos in position:
    account.update(dict({pos['证券代码']: pos}))

# In[]
def order_pct_to(buylist, pct=1):
    '''买卖buylist中的股票，使所有股票占总资产的pct百分比。 各股票市值均等，考虑到佣金，交易额小于2万的不操作'''
    stock_nums = len(buylist)
    money = account['总资产'] * pct / stock_nums
    for stock in buylist:
        stock_value = account.get(stock, dict()).get('市值', 0)
        buy_money = money - stock_value
        # print(money, buy_money, stock_value)
        if buy_money > 20000:
            df = ts.get_realtime_quotes(stock)
            price = float(df.at[0, 'ask'])

            amount = buy_money / price
            amount = int(amount / 100) * 100
            # user.buy(stock, price, amount)
            print("buy", stock, price, amount)

        time.sleep(0.3)

def sell_not_in_list(buylist):
    for pos in position:
        stock = pos.get('证券代码', 0)
        amount = pos.get('可用余额', 0)
        if stock not in buylist and stock != 0 and amount > 0:
            df = ts.get_realtime_quotes(stock)
            price = float(df.at[0, 'bid'])
            # user.sell(stock,price, amount )
            print("sell", stock, price, amount)



buylist = read_ahstock.ReadStockAH().get_buylist()

sell_not_in_list(buylist)
order_pct_to(buylist)

# In[]
