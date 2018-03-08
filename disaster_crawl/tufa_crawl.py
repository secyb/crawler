#-*- coding: UTF-8 -*- 
import re  # 网络连接模块
import bs4  # DOM解析模块
import pymysql  # 数据库连接模块
import urllib2  # 网络访问模块

# 配置参数
maxcount = 1000  # 数据数量
root_url = 'http://www.12379.cn/html/yjxx/yjlb/index.shtml'  # 起始位置

# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '123456',
    'database': 'disater',
    'charset': 'utf8'
}

url_set = set()  # url集合
url_old = set()  # 过期url

# 获取首页链接
#创建request对象
request = urllib2.Request(root_url)
#添加http的header
request.add_header('User-Agent', 'Mozilla/5.0')
#发送请求获取结果
response = urllib2.urlopen(request)
html = response.read().decode('utf-8')
soup = bs4.BeautifulSoup(html, 'html.parser')
#pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'
#pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+\.html'
pattern = '/data/alarmcontent'
links = soup.find_all('a', href=re.compile(pattern))
#links = soup.find_all('a', href=re.compile(r'/data/alarmcontent'))
for link in links:
    print link
    url_set.add(link['href'])


# 文章类定义
class Article(object):
    def __init__(self):
        self.title = None
        self.content = None


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

# 处理URL信息
count = 0
while len(url_set) != 0:
    try:
        # 获取链接
        url = url_set.pop()
        url_old.add(url)

        # 获取代码
        html1 = urllib2.urlopen(url)
        html = html1.read().decode('utf-8')

        # DOM解析
        soup = bs4.BeautifulSoup(html, 'html.parser')
        pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+\.html'
        links = soup.find_all('a', href=re.compile(pattern))

        # 获取URL
        for link in links:
            if link['href'] not in url_old:
                url_set.add(link['href'])

               
        article = Article()
        page = soup.find('div', {'class': 'tgaozhengwen'})
        article.title = page.find('span', {'class': 'tgaozhengwentxet'}).get_text()
        article.content = page.find('span', {'class': 'tgaozhengwen2'}).get_text()

        # 存储数据
        sql = "INSERT INTO tufa( title, content ) "
        sql = sql + " VALUES ('%s', '%s') "
        data = (article.title, article.content)
        cursor.execute(sql % data)
        connect.commit()

    except Exception as e:
        print(e)
        continue
#sql = "INSERT INTO news( url, title, author, date, about, content ) "
#sql = sql + " VALUES ('%s', '%s', '%s', '%s', '%s', '%s') "
#data = ("a", "b", "c", "d", "e", "f")
#cursor.execute(sql % data)
#connect.commit()
# 关闭数据库连接
cursor.close()
connect.close()
'''
Created on 2017年12月16日

@author: liuwei
'''
