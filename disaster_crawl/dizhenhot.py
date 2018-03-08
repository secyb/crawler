import re  # 网络连接模块
import bs4  # DOM解析模块
import pymysql  # 数据库连接模块
import urllib.request  # 网络访问模块

home = 'http://www.cea.gov.cn/publish/dizhenj/464/515/index.html'  # 第一个url
root_url = 'http://www.cea.gov.cn/publish/dizhenj/464/515/index'
url_home =list()  #初始url集合
url_home.append(home)
for index in range(2,81+1):
    url = root_url + '_' + str(index) +'.html'
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
    url_set = list()  # url集合
    home = url_home.pop(0)
    request = urllib.request.Request(home)
    #添加http的header
    request.add_header('User-Agent', 'Mozilla/5.0')
    #发送请求获取结果
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #/publish/dizhenj/464/515/20180305104517289290547/index.html
    pattern = '/publish/dizhenj/464/515/\d+/index\.html'
    #links = soup.find_all('a', href=re.compile(r'/publish/dizhenj/464/479/'))
    links = soup.find_all('a', href=re.compile(pattern))
    for link in links:
        new_url = link['href']
        new_full_url = urllib.parse.urljoin(home, new_url)
        url_set.append(new_full_url)
    '''for link in links:
        print link
        url_set.append(link['href'])
    '''
    
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
            page1 = soup.find('div', {'class': 'detail_main_right_conbg_tit'})
            page2 = soup.find('div', {'class': 'detail_main_right_conbg_con'})
            article.title = page1.find('div', {'style': "text-align:center; font-size:24px;font-weight:bolder;font-family:'黑体';padding-top:5px;"}).get_text()
            article.content = page2.find('div', {'style': 'font-size:16px;'}).get_text()
    
            # 存储数据
            sql = "INSERT INTO dizhenhot( title, content ) "
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
Created on 2018年3月6日

@author: liuwei
'''
