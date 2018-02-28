# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 16:37:43 2016

@author: yangz
"""
import re
import csv
import codecs
import sys
import os
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
def fuzzyfinder(user_input,collection):
    collection=[collection]
    suggestions = []
    pattern = '.*?'.join(user_input)    # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)         # Compiles a regex.
    for item in collection:
        match = regex.search(item)      # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]
def fuzzy_compute(user_input,collection):
    user_input=user_input.replace('大学','')
    user_input=user_input.replace('学院','')
    user_input=user_input.replace('中心','')
    collection=collection.replace('大学','')
    collection=collection.replace('学院','')
    collection=collection.replace('中心','')
    num_fuzzy=0
    word_num=0
    judge=0
    s1=set(jieba.cut(user_input))
    s2=set(jieba.cut(collection))
    s_list=s1 & s2
    word_num=len(s_list)/min(len(set(jieba.cut(user_input))),set(jieba.cut(collection)))
    for str_1 in user_input:
        if str_1 in collection:
            num_fuzzy=num_fuzzy+1
    num_fuzzy=num_fuzzy/min(len(user_input),len(collection))
    for i in range(len(user_input)-2):
        if user_input[:len(user_input)-i] in collection:
            judge=1
    return num_fuzzy,word_num,judge      
def same_name(name_list,adress_list,Name_list,Adress_list,temp):
    Name=[]
    Adress=[]
    tt=name_list[0]        
    temp_name=name_list[0].strip().split(';')
    if temp_name[-1]=='':
        temp_name=temp_name[0:-1]
    for i in range(len(temp_name)):
        for j in range(i+1,len(temp_name)):
            if temp_name[i]==temp_name[j]:
                temp_name[j]=''
    temp_adress=adress_list[0].strip().split(';')
    if temp_adress[-1]=='':
        temp_adress=temp_adress[0:-1]
    for i in range(len(Name_list)):
        Name=Name_list[i].strip().split(';')
        if Name[-1]=='':
            Name=Name[0:-1]
        Adress=Adress_list[i].strip().split(';')
        if Adress[-1]=='':
            Adress=Adress[0:-1]
        judge=0
        for temp2 in temp_adress:
            for temp22 in Adress:
                A=fuzzyfinder(temp2,temp22) 
                if (len(A)>0):
                    judge=1
                else:
                    B=fuzzyfinder(temp22,temp2)
                    if (len(B)>0):
                        judge=1
                    else:
                        C,D,E=fuzzy_compute(temp2,temp22)
                        if (C>=0.3) or (D>=0.3) or (E==1):
                            judge=1
        s1=len(set(temp_name)&set(Name))
        if s1>1:
            judge=1
        for temp1 in temp_name:
            TEMPP=temp1
            num=temp_name.index(temp1)
            for temp2 in Name:
                if temp2.find(temp1)>-1:        
                    if judge==0:
                        temp_num=''
                        temp_txt=''
                        for num_str in temp2:
                            if num_str in ['0','1','2','3','4','5','6','7','8','9']:
                                temp_num=temp_num+num_str
                            else:
                                temp_txt=temp_txt+num_str
                        if len(temp_num)>0:
                            temp_num=int(temp_num)+1
                            TEMPP=temp_txt+str(temp_num)
                        else:
                            TEMPP=temp_txt+str(1)
                    else:
                        TEMPP=temp2
            temp_name[num]=TEMPP
    txt=''    
    for name in temp_name:
        txt=txt+name+';'
    if len(txt)>0:
        name_list=[txt]
    else:
        name_list=[]
    temp=temp.replace(tt,txt,1)
    return name_list,temp
def match_title_name(new_txt,temp,name_list,title_list,adress_list,year_list,Name_list,Title_list,Adress_list,Year_list):
    temp_txt=''
    if title_list[0] in Title_list:
        index=Title_list.index(title_list[0])
        judge=1
        t1=name_list[0].strip().split(';')[0:-1]
        t2=Name_list[index].strip().split(';')[0:-1]
        for tt in t1:
            if tt not in t2:
                judge=0
        if judge==1:#二者一样合并
            if Year_list[index]=='NA':
                if 'NA' not in year_list:
                    index1=new_txt.find(Name_list[index])
                    temp_txt=new_txt[index1:]
                    index2=temp_txt.find('YR ')
                    temp_txt=temp_txt[0:index2]+temp_txt[index2:].replace(Year_list[index],year_list[0],1)
                    index2=temp_txt.find('AD ')
                    temp_txt=temp_txt[0:index2]+temp_txt[index2:].replace(Adress_list[index],adress_list[0],1)
                    new_txt=new_txt[0:index1]+temp_txt
                    Year_list[index]=year_list[0]
                    Adress_list[index]=adress_list[0]
            else:
                if 'NA' not in year_list:
                    if int(Year_list[index])>int(year_list[0]):
                        index1=new_txt.find(Name_list[index])
                        temp_txt=new_txt[index1:]
                        index2=temp_txt.find('YR ')
                        temp_txt=temp_txt[0:index2]+temp_txt[index2:].replace(Year_list[index],year_list[0],1)
                        index2=temp_txt.find('AD ')
                        temp_txt=temp_txt[0:index2]+temp_txt[index2:].replace(Adress_list[index],adress_list[0],1)
                        new_txt=new_txt[0:index1]+temp_txt                        
                        Year_list[index]=year_list[0]
                        Adress_list[index]=adress_list[0]
        else:
            Title_list.extend(title_list)
            Adress_list.extend(adress_list)
            Year_list.extend(year_list)
            Name_list.extend(name_list)
            new_txt=new_txt+'\n'+temp+'DS CNKI'
    else:
        Title_list.extend(title_list)
        Adress_list.extend(adress_list)
        Year_list.extend(year_list)
        Name_list.extend(name_list)
        new_txt=new_txt+'\n'+temp+'DS CNKI'      
    return new_txt,Name_list,Title_list,Adress_list,Year_list           
#提取T1 AD YR A1
def sub_func(temp):
    title_list=[]
    adress_list=[]
    year_list=[]
    name_list=[]
    reg=r'A1 (.*?)\n'
    name_re=re.compile(reg)
    name_list=re.findall(name_re,temp)
    if (len(name_list)>0):
        if(name_list[0].find('佚名')==-1)&(name_list[0].find('本刊')==-1):
            if (len(name_list)>1):
                name_list=[name_list[0]]
            name_list[0].replace('指导:','')
            name_list[0].replace('指导：','')
            reg=r'T1 (.*?)\n'
            title_re=re.compile(reg)
            title_list=re.findall(title_re,temp)
            if(len(title_list)>0):
                if (len(title_list)>1):
                    title_list=[title_list[0]]
                reg=r'AD (.*?)\n'
                adress_re=re.compile(reg)
                adress_list=re.findall(adress_re,temp)
                if len(adress_list)>1:
                    adress_list=[adress_list[0]]
                if len(adress_list)==0:
                    adress_list=['NA']
                reg=r'YR (.*?)\n'
                year_re=re.compile(reg)
                year_list=re.findall(year_re,temp)
                if len(year_list)>1:
                    year_list=[year_list[0]]
                if len(year_list)==0:
                    year_list=['NA']
            else:
                name_list=[]
                title_list=[]
                
        else:
            name_list=[]
    else:
        name_list=[]
    return name_list,title_list,adress_list,year_list
def names_func(filename,path_now):
    Title_list=[]#初始化，名称标题
    Adress_list=[]#单位
    Year_list=[]#年份
    Name_list=[]#作者
    new_txt=''
    filename_txt=filename+'.txt'#打开txt文件
    f = open(filename_txt) 
    g=f.read()#存放文件字符串
    f.close()
    temp_len=len('DS CNKI')
    index_temp=g.find('DS CNKI')#发现LA
    temp=g[0:index_temp]
    while index_temp>-1:
        name_list,title_list,adress_list,year_list=sub_func(temp)
        if (len(title_list)>0)&(len(adress_list)>0)&(len(name_list)>0)&(len(year_list)>0):
            if (name_list[0].find("课题组")>-1) or (name_list[0].find("中心")>-1) or (name_list[0].find("团队")>-1):
                temp=temp+'\n'
                f=file(path_now+filename+unicode('_课题组等.txt','utf-8').encode('gbk'),'a')
                f.write(temp)
                f.close()
                temp=''
                name_list=[]
                title_list=[]
                adress_list=[]
                year_list=[]
        if (len(title_list)>0)&(len(adress_list)>0)&(len(name_list)>0)&(len(year_list)>0):
            name_list,temp=same_name(name_list,adress_list,Name_list,Adress_list,temp)
            new_txt,Name_list,Title_list,Adress_list,Year_list=match_title_name(new_txt,temp,name_list,title_list,adress_list,year_list,Name_list,Title_list,Adress_list,Year_list)
        g=g.replace(g[0:index_temp+temp_len],'')
        index_temp=g.find('DS CNKI')
        temp=g[0:index_temp]
        temp=temp
    filename_csv=path_now+filename+'_names.csv'
    f=file(filename_csv,'wb')
    f.write(codecs.BOM_UTF8)
    names_csv= csv.writer(f,dialect='excel')
    for name in Name_list:
        t=name.strip().split(';')[0:-1]
        if len(t)==1:
            names_csv.writerow(t)
        else:
            for j in range(len(t)-1):
                names_csv.writerow(t[j:])
    f.close()
    filename_csv=path_now+filename+'_data.csv'
    f=file(filename_csv,'wb')
    f.write(codecs.BOM_UTF8)
    data_csv= csv.writer(f,dialect='excel')
    data_csv.writerow(['题目T1','作者A1','地址AD','年份YR'])
    for i in range(len(Title_list)):
        data_csv.writerow([Title_list[i],Name_list[i],Adress_list[i],Year_list[i]])
    f.close()
    filename_new_txt=path_now+filename+'_new.txt'
    f=file(filename_new_txt,'w')
    f.write(new_txt)
    f.close()
    print unicode('处理完毕','utf-8').encode('gbk')
answer='Y'
while answer==('Y' or 'y'):
    path_now=os.getcwd()
    filename=raw_input(unicode('请输入文件的名字（不包括扩展名）: ','utf-8').encode('gbk'))
    path_now=path_now+'\\'+filename
    if os.path.exists(path_now):
        print unicode('已经存在'+filename+'目录.','utf-8').encode('gbk')
        TEMP=raw_input(unicode('是否重新命名一个目录（Y/N）:','utf-8').encode('gbk'))
        if TEMP==('Y' or 'y'):
            TEMP_NAME=raw_input(unicode('请输入新目录名字（谢绝中文）：','utf-8').encode('gbk'))
            path_now=os.getcwd()
            path_now=path_now+'\\'+TEMP_NAME
            os.mkdir(path_now)
    else:
        os.mkdir(path_now)
    path_now=path_now+'\\'
    names_func(filename,path_now)
    answer=raw_input(unicode('结果已经存放至'+filename+'文件夹下。\n'+'是否继续执行（Y/N）: ','utf-8').encode('gbk'))
