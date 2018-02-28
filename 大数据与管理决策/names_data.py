# -*- coding: utf-8 -*-
#coding=utf-8
"""
Created on Mon Dec 26 19:51:58 2016

@author: yangz
"""
import re
import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def names_func(filename):
    filename_txt=filename+'.txt'
    f = open(filename_txt) 
    reg=r'A1(.*?)\n'
    name_re=re.compile(reg)
    name_list=re.findall(name_re,f.read())
    f.close()
    filename_csv=filename+'.csv'
    f=open(filename_csv,'wb')
    f.write(codecs.BOM_UTF8)
    names_csv= csv.writer(f,dialect='excel')
    for name in name_list:
        t=name.strip().split(';')[0:-1]
        if len(t)>1:
            for j in range(len(t)-1):
                names_csv.writerow(t[j:])
    f.close()
    print unicode('处理完毕','utf-8').encode('gbk')
answer='Y'
while answer==('Y' or 'y'):
    filename=raw_input(unicode('请输入文件的名字（不包括扩展名）: ','utf-8').encode('gbk'))
    names_func(filename)
    answer=raw_input(unicode('是否继续执行（Y/N）: ','utf-8').encode('gbk'))
