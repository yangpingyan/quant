#!/usr/bin/env python 
# coding: utf-8
# @Time : 2018/10/24 10:09 
# @Author : yangpingyan@gmail.com

from . import read_ahstock

buylist = read_ahstock.ReadStockAH().get_buylist()
print(buylist)

# In[]