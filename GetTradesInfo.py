# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 14:18:11 2017

@author: yangp
"""


'''
Created on 2017-4-6

@author: James
'''

from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import datetime
import pandas as pd
import os
import string
import re
import logging



def getAllExcelFiles(file_dir):
    L = []
#    for root, dirs, files in os.walk(file_dir):
    files = os.listdir(file_dir)
    for file in files:
        if os.path.splitext(file)[1] == '.xlsx' \
            and file.startswith('LB') is False \
            and file.startswith('LS') is False \
            and file.startswith('1') is False \
            and file.startswith('.') is False \
            and file.startswith('~') is False:
            L.append(os.path.join(file_dir, file))
    return L

if __name__ == '__main__':
    logger = logging.getLogger("GetTradesInfo")
    logger.setLevel(logging.DEBUG)  
    files = getAllExcelFiles(".")
    print("统计的账户个数是{}个".format(len(files)))

    logger.debug(files)

    all_df = pd.DataFrame()
    for excelfile in files:
        print(excelfile)
        sheet_list = ['交割单', '当日成交']
        for sheet_name in sheet_list :
            df_file = pd.read_excel(excelfile, sheet_name=sheet_name, header=0)
            if '成交金额' in df_file.columns and '发生金额' in df_file.columns :
                df_file.drop(['发生金额'], axis=1, inplace=True)
            df_file = df_file.dropna(how='all')
         
            df_file.rename(columns={'委托类别':'操作', '买入标志':'操作', \
                                    '买卖标志':'操作', '成交均价':'成交价格', \
                                    '发生金额':'成交金额','交割日期':'成交日期',\
                                    '股票名称':'证券名称','买卖类型':'操作',\
                                    '业务名称':'操作','发生日期':'成交日期',\
                                    '交易日期':'成交日期',}, inplace = True)
            df_file = df_file[['成交日期', '证券名称', '操作', '成交数量', '成交价格', '成交金额']]
            df_file = df_file.dropna(subset=['证券名称', '成交数量', '成交金额'])
            if(df_file.empty):
                continue
            df_file = df_file[df_file['证券名称'] == '雷科防务']
            if(df_file.empty):
                continue
            account_name = re.findall(r"\w{1,}-[\u4e00-\u9fa5]{1,}-[\u4e00-\u9fa5]{1,}", excelfile)
            df_file['账户'] = "".join(account_name)
    
            all_df = pd.concat([all_df, df_file], join='outer', axis=0, ignore_index=True)
      

    all_df['成交日期'] = [x if isinstance(x,str) else "%d"%x for x in all_df['成交日期']]
    all_df['成交数量'] = all_df['成交数量'].apply(lambda x:abs(x))
    account_list = list(set(all_df['账户']))
#    print(all_df)

    #取得合计持股数，与实际持股数核对以判断取得全部数据
    buy_df = all_df[all_df['操作'].str.contains('买入')]
    buy_amount = buy_df['成交数量'].sum()
    sell_df = all_df[all_df['操作'].str.contains('卖出')]
    sell_amount = sell_df['成交数量'].sum()
    print("总持股合计={:,.0f}".format(buy_amount-sell_amount))

    #按日期取得交易数据
    acount_list = list(set(all_df['账户']))
    date_str = '20180518'
    date_df = all_df[all_df['成交日期'].str.contains(date_str)]
    buy_df = date_df[date_df['操作'].str.contains('买入') ]
    buy_amount = buy_df['成交数量'].sum()
    sell_df = date_df[date_df['操作'].str.contains('卖出') ]
    sell_price_min = sell_df['成交价格'].min()
    sell_min_df = sell_df[sell_df['成交价格'] == sell_price_min ]
   
    sell_amount = sell_df['成交数量'].sum()
    print("{}情况如下：".format(date_str))
    print("  账户{}卖出{}股最低价格{}".format(set(sell_min_df['账户']), sell_min_df['成交数量'].sum(), sell_price_min))
    print("  合计买入{:,.0f}股，卖出{:,.0f}股，共增持股{:,.0f}股。其中：".format(buy_df['成交数量'].sum(), \
          sell_df['成交数量'].sum(), buy_df['成交数量'].sum()-sell_df['成交数量'].sum()))
    
    for account in account_list :
        buy_amount = buy_df[buy_df['账户'] == account]['成交数量'].sum()
        sell_amount = sell_df[sell_df['账户'] == account]['成交数量'].sum()
        if buy_amount>0 or sell_amount>0 :
            print("    账户{}合计买入{:,.0f}股，卖出{:,.0f}股，共增持{:,.0f}股".format(account, buy_amount, sell_amount, buy_amount-sell_amount ))
        
#    print(date_df)

    #按账户取得交易数据
    
#    for account_str in account_list:
#        tmp_df = all_df[all_df['账户'].str.contains(account_str)]
#        buy_df = tmp_df[tmp_df['操作'].str.contains('买入') ]
#        buy_amount = buy_df['成交数量'].sum()
#        sell_df = tmp_df[tmp_df['操作'].str.contains('卖出') ]
#        sell_amount = sell_df['成交数量'].sum()
#        print("{}买入股数合计={:,.0f}".format(account_str,buy_amount))
#        print("{}卖出股数合计={:,.0f}".format(account_str,sell_amount))
#        print("{}持股合计={:,.0f}".format(account_str,(buy_amount - sell_amount)))
    print("mission complete")











