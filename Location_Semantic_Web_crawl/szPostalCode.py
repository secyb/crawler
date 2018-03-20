import re  # 网络连接模块
import bs4  # DOM解析模块
import pymysql  # 数据库连接模块
import urllib.request  # 网络访问模块

luohu = 'https://www.youbianku.com/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3%E5%B8%82%E7%BD%97%E6%B9%96%E5%8C%BA'
futian = 'https://www.youbianku.com/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3%E5%B8%82%E7%A6%8F%E7%94%B0%E5%8C%BA'
nanshan = 'https://www.youbianku.com/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3%E5%B8%82%E5%8D%97%E5%B1%B1%E5%8C%BA'
baoan = 'https://www.youbianku.com/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3%E5%B8%82%E5%AE%9D%E5%AE%89%E5%8C%BA'
longgang = 'https://www.youbianku.com/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3%E5%B8%82%E9%BE%99%E5%B2%97%E5%8C%BA'
yantian = 'https://www.youbianku.com/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3%E5%B8%82%E7%9B%90%E7%94%B0%E5%8C%BA'

url_home =list()  #初始url集合

url_home.append(luohu)
url_home.append(futian)
url_home.append(nanshan)
url_home.append(baoan)
url_home.append(longgang)
url_home.append(yantian)

# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '123456',
    'database': 'wzyyw',
    'charset': 'utf8'
}

# 文章类定义
class Article(object):
    def __init__(self):
        self.addressRegion = None
        self.addressLocality1 = None
        self.addressLocality2 = None
        self.streetAddress = None
        self.postalCode = None

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
    url_set = list()  # url集合
    home = url_home.pop(0)
    request = urllib.request.Request(home)
    #添加http的header
    request.add_header('User-Agent', 'Mozilla/5.0')
    #发送请求获取结果
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    pattern = '/%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5.*'
    links = soup.find_all('a', href=re.compile(pattern))
    for link in links:
        new_url = link['href']
        new_full_url = urllib.parse.urljoin(home, new_url)
        url_set.append(new_full_url)
    
    
    # 处理URL信息
    while len(url_set) != 0:
        try:
            # 获取链接
            url = url_set.pop(0)
    
            request = urllib.request.Request(url)
            #添加http的header
            request.add_header('User-Agent', 'Mozilla/5.0')
            #发送请求获取结果
            response = urllib.request.urlopen(request)
            # 获取代码
            #html1 = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')
    
            # DOM解析
            soup = bs4.BeautifulSoup(html, 'html.parser')
            article = Article()
            page = soup.find('div', {'class': 'left'})
            article.addressRegion = page.find('span', {'itemprop': 'addressRegion'}).get_text()
            addressLocality = page.find_all('span', {'itemprop': 'addressLocality'})
            article.addressLocality1 = addressLocality[0].get_text()
            article.addressLocality2 = addressLocality[1].get_text()
            article.streetAddress = page.find('span', {'itemprop': 'streetAddress'}).get_text()
            article.postalCode = page.find('span', {'itemprop': 'postalCode'}).get_text()

            # 存储数据
            sql = "INSERT INTO shenzhen( addressRegion, dishi, quxian, streetAddress, postalCode ) "
            sql = sql + " VALUES ('%s', '%s', '%s', '%s', '%s') "
            data = (article.addressRegion, article.addressLocality1, article.addressLocality2, article.streetAddress, article.postalCode)
            cursor.execute(sql % data)
            connect.commit()
    
        except Exception as e:
            print(e)
            continue
# 关闭数据库连接
cursor.close()
connect.close()
'''
Created on 2018年3月19日

@author: liuwei
'''
