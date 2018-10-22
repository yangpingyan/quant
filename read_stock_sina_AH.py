#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/10/21 20:21 
# @Author : yangpingyan@gmail.com
import re
import urllib

url_pre = 'http://hq.sinajs.cn/rn=&list='
# code = 'rt_hkhqtime,s_sh000001,s_sz399001,rt_hkHSI,rt_hkHSCEI,HKDCNY,s_sh000905,s_sh000300,sh601318,sz000001'
code = 'sh601318'
url = url_pre + code

response = urllib.request.urlopen(url)
rep_data = response.read().decode("gbk")
stocks_detail = "".join(rep_data)
grep_str = re.compile(r"(\d+)=([^\s][^,]+?)%s%s" % (r",([\.\d]+)" * 29, r",([-\.\d:]+)" * 2))
grep_str = re.compile(r"(\d+)=([^\s][^,]+?)" )
result = grep_str.finditer(stocks_detail)
all = grep_str.findall(stocks_detail)
len(all)

url_ahstocks = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/var%20hk_corrastock=/HK_CorrStock.getCorrstock'
response = urllib.request.urlopen(url_ahstocks)
rep_data = response.read().decode("gbk")
stocks_detail = "".join(rep_data)
grep_str = re.compile(r"(\w+)=\(\(")
all = grep_str.findall(stocks_detail)