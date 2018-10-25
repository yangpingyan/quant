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

easytrader.
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

def sell_not_in_list(buylist):
    for pos in position:
        stock = pos.get('证券代码', 0)
        amount = pos.get('股票余额', 0) - 100  # 留100股
        value = pos.get('市值', 0)
        if stock not in buylist and value > 20000 and amount > 0:
            df = ts.get_realtime_quotes(stock)
            price = float(df.at[0, 'bid'])
            # user.sell(stock,price, amount )
            print("sell", stock, price, amount)
            time.sleep(0.3)


def order_pct_to(buylist, pct=0.8):
    '''买卖buylist中的股票，使所有股票占总资产的pct百分比。 各股票市值均等，考虑到佣金，交易额小于2万的不操作'''
    if len(buylist) < 1:
        return
    stock_nums = len(buylist)
    money = account['总资产'] * pct / stock_nums
    # 先卖持仓过多的股票
    for stock in buylist:
        stock_value = account.get(stock, dict()).get('市值', 0)
        buy_money = money - stock_value
        df = ts.get_realtime_quotes(stock)
        if buy_money < -20000:
            price = float(df.at[0, 'bid'])
            buy_money = -buy_money
            amount = buy_money / price
            amount = int(amount / 100) * 100
            # user.sell(stock, price, amount)
            print("sell", stock, price, amount)
            time.sleep(0.3)

    # 再买入buylist中的股票
    for stock in buylist:
        stock_value = account.get(stock, dict()).get('市值', 0)
        buy_money = money - stock_value
        df = ts.get_realtime_quotes(stock)
        if buy_money > 20000:
            price = float(df.at[0, 'ask'])
            amount = buy_money / price
            amount = int(amount / 100) * 100
            # user.buy(stock, price, amount)
            print("buy", stock, price, amount)
            time.sleep(0.3)



buylist = read_ahstock.ReadStockAH().get_buylist()
print('buylist :', buylist)
sell_not_in_list(buylist)
order_pct_to(buylist)

# In[]
buylist = ['601318', '000001', '000002']
print('buylist :', buylist)
sell_not_in_list(buylist)
order_pct_to(buylist)

