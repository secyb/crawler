import tweepy  
  
#填写twitter提供的开发Key和secret  
consumer_key = '#'  
consumer_secret = '#'  
access_token = '#'  
access_token_secret = '#'  
  
#提交你的Key和secret  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  
  
#获取类似于内容句柄的东西  
api = tweepy.API(auth,proxy="127.0.0.1:1080")  
#39.101938 -80.408834 1km
index = 1014149304498483201
id_str = 842740482505654272
for tweet in api.search(q="-Liuwei",lang="English",max_id=index-1,count=2):
    print(tweet)
'''
Created on 2018年6月25日

@author: liuwei
'''
