#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/10/21 20:21 
# @Author : yangpingyan@gmail.com
import urllib.request
from bs4 import BeautifulSoup

response = urllib.request.urlopen("http://finance.sina.com.cn/stock/hkstock/anh.shtml")
html = response.read().decode("gbk")
soup = BeautifulSoup(html)
print(soup.prettify())
div = soup.find_all( id = 'table_container')
a_bf = BeautifulSoup(str(div[0]))
a = a_bf.find_all('a')
for each in a:
    print(each.string, each.get('href'))
    break
