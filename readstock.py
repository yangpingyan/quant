'''
Created on 2016-8-25

@author: Administrator
'''
import datetime
import tushare as ts
import pandas as pd  
import time

# time.strptime('2008-02-14', '%Y-%m-%d')
def readstock1(stockid='399300', start='2016-01-01', end=None):
    df = ts.get_hist_data('399300', start=start, end=end)
    return df

def readstock():    
    df = ts.get_realtime_quotes('hs300')
    price = df['price'][0]
    return price


if __name__ == '__main__':
    df = readstock()
    print(df)
    print("over")
  
#
#    now = datetime.datetime.today()
#    start = end = now.strftime('%Y-%m-%d')
#    import pandas as pd  
#    import numpy as np  
#    data = {'state':['Ohino','Ohino','Ohino','Nevada','Nevada'],
#            'year':[2000,2001,2002,2001,2002],
#            'pop':[1.5,1.7,3.6,2.4,2.9]}
#    df = pd.DataFrame(data)
#    df = pd.DataFrame(data,index=['one','two','three','four','five'],
#                   columns=['year','state','pop','debt'])  
#    # For .read_csv, always use header=0 when you know row 0 is the header row  
#    df = pd.read_csv('D:\stockhistory\day\data/002790.csv', header=0)  
#    print(df)
#    df.index
#    df.columns
#    print(df[['date','close', 'volume']])
#    print(df[df['date']>'2016-03-15'])
#    print(df[df['date']>'2016-03-15'][['date','close']])
#    print(df[df['close'].isnull()][['date','close']])
#    print(df[ (df['date']>'2016-03-15') & (df['close']>45) ])
#    print(df.head(3))
#    print(df.tail(3))
#    print(df.dtypes)
#    print(df.info())
#    print(df.describe())
#    print(df['close'].mean())
#    df.reindex(index=[5,4,3],columns=None,method='ffill')
#    df.drop(2)
#    df.ix[:2, :2]
#    df.add(df1, fill_value=0)
#    df.sub(df1, fill_value=0)
#    df.apply(func, axis=0)
#    df.sort_index(axis=0, by='close', ascending=True)
#    
#    
#    s = pd.Series([1,2,3.0,'abc'])
#    s = pd.Series(data=[1,3,5,7],index = ['a','c','d','b'])
#    s.index
#    s.values
#    s.name = 'a_series'
#    s.index.name = 'letter'
#    a = ['a','b','c','d','e']
#    s.reindex(a)
#    s.reindex(a, fill_value=0, method='ffill')
#    s.rank(method='average', ascending=True)
#    
#    print("game over")