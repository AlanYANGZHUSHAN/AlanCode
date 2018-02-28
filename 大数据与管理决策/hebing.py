# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 14:52:53 2017

@author: yangz
"""
year=range(2008,2017)
temp_txt=''
for y in year:
    filename=str(y)+'.txt'
    f=open(filename,'r')
    temp_txt=temp_txt+f.read()
    f.close()
filename='total_data.txt'
f=open(filename,'w')
f.write(temp_txt)
f.close()