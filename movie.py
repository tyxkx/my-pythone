# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:14:24 2019

@author: fanrui3
"""

import numpy as np
import pandas
from sklearn.metrics.pairwise import cosine_similarity

max_same=0.7    #相似度要求大于0.7
best_vote=3     #推荐分数在3分以上
#读取数据
data = pandas.read_csv('H:/ml-latest-small/ratings.csv',encoding='GBK').fillna(0)

#初始化数组
moviedata=np.zeros((max(data['userId']),max(data['movieId'])), dtype=np.int32)
sim_user=[]

#形成打分表
for i in data.values:
   moviedata[int(i[0])-1,int(i[1])-1]=i[2]
#计算相似度
user_sim=cosine_similarity(moviedata)


#形成相似度大于0.7的关联相似用户表
for i in range(len(user_sim)):
   for j in range(len(user_sim[0])):
       if user_sim[i,j]>max_same and user_sim[i,j]!=1 and i!=j:
          sim_user.append([i+1,j+1,user_sim[i,j]])
          
#按条检索相似用户，打分大于3分以上的用户进行推荐
#形成A用户和B用户的打分表

for i in range(len(sim_user)):
    data1 =data[(data['userId'] == sim_user[i][0]) & (data['rating'] > best_vote)]
    data2 =data[(data['userId'] == sim_user[i][1]) & (data['rating'] > best_vote)]

#方法二：使用dataframe 差集
    result = pandas.DataFrame(data1).append(data2)
    result=result.drop_duplicates(subset=['movieId'],keep=False)
   # 将1用户和2用户的打分推荐并在一起，滤重
    for n in result.values:
        if n[0] == sim_user[i][1]:   
   #如果滤重后的userId与用户列表中的B相等，则把对应的影片推荐给A
           lstr=str(int(sim_user[i][0]))+'|'+str(int(n[1]))+'\n'
           fl=open('h:/movie.txt', 'a+')
           fl.write(lstr)
           fl.close()
           lstr='' 
  '''
#方法一：循环实现
  #对应A用户的影片检索B用户是否也看过

    for m in data1.values:
        cnt=0      #记数
        for n in data2.values:
            if n[1] == m[1]:        #两人都看过，不推荐，跳出
                cnt = 0 
                break
            if cnt==len(data2) -1 :   #到达队列的底部，B用户没有看过A用户的影片，推荐
                lstr=str(int(n[0]))+'|'+str(int(m[1]))+'\n'
                fl=open('h:/movie.txt', 'a+')
                fl.write(lstr)
                fl.close()
            cnt+=1        #记数加1


'''
