import re  # 网络连接模块
import bs4  # DOM解析模块
import pymysql  # 数据库连接模块
import urllib.request  # 网络访问模块

#home = 'http://www.jianzai.gov.cn/DRpublish/ywcp/000100040002-1.html'  # 起始位置
origin_url = 'http://www.jianzai.gov.cn/DRpublish/ywcp/000100040002-'
#url_home =set()  #初始url集合
url_home =list()  #初始url集合

for index in range(1,82+1):
    url = origin_url + str(index) +'.html'
    url_home.append(url)


# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '123456',
    'database': 'disater',
    'charset': 'utf8'
}

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

while len(url_home) != 0:
    # 获取首页链接
    #创建request对象
    #url_set = set()  # url集合
    url_set = list()  # url集合
    home = url_home.pop(0)
    request = urllib.request.Request(home)
    #添加http的header
    request.add_header('User-Agent', 'Mozilla/5.0')
    #发送请求获取结果
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    #print html
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'
    pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+\.html'
    #pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+'
    links = soup.find_all('a', href=re.compile(pattern))
    for link in links:
        url_set.append(link['href'])
    
    
    # 处理URL信息
    while len(url_set) != 0:
        try:
            # 获取链接
            url = url_set.pop(0)
    
            # 获取代码
            html1 = urllib.request.urlopen(url)
            html = html1.read().decode('utf-8')
    
            # DOM解析
            soup = bs4.BeautifulSoup(html, 'html.parser')
            article = Article()
            page = soup.find('div', {'class': 'tgaozhengwen'})
            article.title = page.find('span', {'class': 'tgaozhengwentxet'}).get_text()
            #txt = page.find('span', {'class': 'tgaozhengwen2'})
            article.content = page.find('span', {'class': 'tgaozhengwen2'}).get_text()
            #article.content = txt.find('p', {'style': 'text-indent'}).get_text()
            #article.content = txt.find('p', style=re.compile(r'.*?')).get_text()
            #article.content = txt.find('span', style=re.compile(r'.*?')).get_text()
    
            # 存储数据
            sql = "INSERT INTO jianzai( title, content ) "
            sql = sql + " VALUES ('%s', '%s') "
            data = (article.title, article.content)
            cursor.execute(sql % data)
            connect.commit()
    
        except Exception as e:
            print(e)
            continue
# 关闭数据库连接
cursor.close()
connect.close()
'''
Created on 2017年12月14日

@author: liuwei
'''
