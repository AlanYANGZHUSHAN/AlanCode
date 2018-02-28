# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 13:59:24 2016

@author: yangz
"""
#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
import requests
import sys
import urllib
import time
import socket
import os
import codecs
os.chdir('C:\Users\yangz\Desktop\pacong3')
reload(sys)
sys.setdefaultencoding("utf-8")
def html_re(url,d,i,sleep_download_time,timeout):
    U=[]
    try:
        time.sleep(sleep_download_time)
        socket.setdefaulttimeout(timeout)
        user_agent = 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
        headers = {'User-Agent' : user_agent,'Referer':url+'/'}
        r = requests.get(url,headers=headers)
        data = r.text
        r.close()
        pic_floder=[]
        pic_url=re.findall('src="(.*?)"',data,re.S)
        for pic in pic_url:
            if pic.find('http://www.cccchzmb.com/userfiles/image/')==-1:
                    if pic.find('site_media/images/')>-1:              
                        f=file(pic,'w')
                        urllib.urlretrieve('http://www.cccchzmb.com/'+pic,pic)
                        f.close()
            else:
                i=i+1
                pic_floder.append('userfiles/image/'+str(i)+pic[-4:])
                data=data.replace(pic,pic_floder[-1]) 
                f=file(pic_floder[-1],'w')
                urllib.urlretrieve(pic,pic_floder[-1])
                f.close()
        f=codecs.open(d+'.html','w','gbk')
        for line in data:
            f.write(line)
        f.close()
    except requests.RequestException as e:
        print(e)
        U=url
    except requests.exceptions.ConnectionError as e:
        print(e)
        U=url
    except UnicodeDecodeError as e:
        print('-----UnicodeDecodeErrorurl:',url)
        U=url
    except socket.timeout as e:
        print("-----socket timout:",url)
        U=url
    except IOError as e:
        print("download ",url,"\nerror:",e)
        U=url
    return i,U
def main_support(i,j,link_list,link_name,sleep_download_time,timeout):
    link_defeat_list=[]
    n=j
    for k in range(n,len(link_list)):
        [i,U]=html_re(link_list[k],link_name[k],i,sleep_download_time,timeout)
        j=j+1
        if len(U)>0:
            link_defeat_list.append(U)
            f=open('link_defeat_list.txt','a')
            f.write(U+'\n')
            f.close()
        print '第'+str(j)+'个网页'
    return i,j,link_defeat_list
f=open('link_name.txt','r')
data=f.readlines()
f.close
link_name=[]
for line in data:
    link_name.append(line.strip())
f=open('link.txt','r')
data=f.readlines()
f.close   
link_list=[]
for line in data:
    link_list.append(line.strip())
i=0
timeout = 20
sleep_download_time=2
link_defeat_list=[]
j=0
[i,j,link_defeat_list]=main_support(i,j,link_list,link_name,sleep_download_time,timeout)