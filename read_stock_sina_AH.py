#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/10/21 20:21 
# @Author : yangpingyan@gmail.com
import re
import urllib

from bs4 import BeautifulSoup

url_pre = 'http://hq.sinajs.cn/rn=&list='
# code = 'rt_hkhqtime,s_sh000001,s_sz399001,rt_hkHSI,rt_hkHSCEI,HKDCNY,s_sh000905,s_sh000300,sh601318,sz000001'
code = 'sh601318'
url = url_pre + code

response = urllib.request.urlopen(url)
rep_data = response.read().decode("gbk")

stocks_detail = "".join(rep_data)
grep_str = re.compile(r"(\d+)=([^\s][^,]+?)%s%s" % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2))
result = grep_str.finditer(stocks_detail)
all = grep_str.findall(stocks_detail)
len(all)
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
