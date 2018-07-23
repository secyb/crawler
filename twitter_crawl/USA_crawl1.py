import tweepy  
import re  # 网络连接模块
import pymysql  # 数据库连接模块
import time
  
#填写twitter提供的开发Key和secret  
consumer_key = '#'  
consumer_secret = '#'  
access_token = '#'  
access_token_secret = '#'  

# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '123456',
    'database': 'python',
    'charset': 'utf8'
}
  
#提交你的Key和secret  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  

# 连接数据库
connect = pymysql.Connect(
    host=db_config['host'],
    port=int(db_config['port']),
    user=db_config['username'],
    passwd=db_config['password'],
    db=db_config['database'],
    charset=db_config['charset']
)
cursor = connect.cursor()

temp_index = 1014149304498483201 

while(1==1):
    index = int(temp_index)  
    try:
        #获取类似于内容句柄的东西  
        api = tweepy.API(auth,proxy="127.0.0.1:1080")  
        #39.101938 -80.408834 1km
        #id_str = 842740482505654272
        #1014133026689830912
        for tweet in api.search(q="-Liuwei",lang="English",max_id=index-1,count=2):
            #print(tweet)
            # 存储数据
            #sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            #cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
            #sql = "INSERT INTO twittertest('content') VALUES (%s)"
            sql = "INSERT INTO twittertest( content ) "
            sql = sql + " VALUES (%s) "
            #data = (tweet)
            tweet = str(tweet)
            cursor.execute(sql,tweet)
            connect.commit()
        time.sleep(6)
        pattern = re.compile(r"id':\s(\d+)")
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        mat = re.search(pattern,tweet)
        temp_index = mat.group(1)
    
    except Exception as e:
        print(e)
        continue