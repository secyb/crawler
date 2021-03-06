import re  # 网络连接模块
import bs4  # DOM解析模块
import pymysql  # 数据库连接模块
#import urllib2  # 网络访问模块
#import urllib  # 网络访问模块
import urllib.request
import time
#import urlparse #urlparse并入了urllib

home = 'http://www.cea.gov.cn/publish/dizhenj/464/479/index.html'  # 第一个url
root_url = 'http://www.cea.gov.cn/publish/dizhenj/464/479/index'
url_home =list()  #初始url集合
url_old = set()
url_home.append(home)
for index in range(2,374+1):
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
def sleeptime(hour,minute,sec):
    return hour*3600 + minute*60 + sec
interval = sleeptime(24,0,0);

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
    #request = urllib2.Request(home)
    request = urllib.request.Request(home)
    #添加http的header
    request.add_header('User-Agent', 'Mozilla/5.0')
    #发送请求获取结果
    #response = urllib2.urlopen(request)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'
    #pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+\.html'
    #pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+'
    pattern = '/publish/dizhenj/464/479/\d+/index\.html'
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
            url_old.add(url)
    
            # 获取代码
            html1 = urllib.request.urlopen(url)
            html = html1.read().decode('utf-8')
    
            # DOM解析
            soup = bs4.BeautifulSoup(html, 'html.parser')
            article = Article()
            page1 = soup.find('div', {'class': 'detail_main_right_conbg_tit'})
            page2 = soup.find('div', {'class': 'detail_main_right_conbg_con'})
            article.title = page1.find('div', {'style': "text-align:center;font-size:24px;padding-top:5px 0;font-weight:bolder;font-family:'黑体';"}).get_text()
            article.content = page2.find('div', {'style': 'font-size:16px;'}).get_text()
            # 将正则表达式编译成Pattern对象
            #时间
            pattern1 = re.compile(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}')
            #地点
            pattern2 = re.compile(r'分(.+)发')
            pattern3 = re.compile(r'\d+\.\d+')
            # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            mat1 = re.search(pattern1,article.content)
            time1 = mat1.group(0)
            mat2 = re.search(pattern2,article.title)
            #mat2 = re.search(pattern2,article.title.encode('utf-8'))
            location = mat2.group(1)
            #location = unicode(mat2.group(1), "utf-8")
            mat3 = re.findall(pattern3,article.content)
            zhenji = mat3[0]
            latitude = mat3[1]
            longitude = mat3[2]
            depth = mat3[4]
            sql = "INSERT INTO dizhenparse2( time, location, zhenji, latitude, longtitude, depth ) "
            sql = sql + " VALUES ('%s', '%s', '%s', '%s', '%s', '%s') "
            data = (time1, location, zhenji, latitude, longitude, depth)
            cursor.execute(sql % data)
            connect.commit()
            #print mat1.group(0)
            #print mat2.group(1)
            #pattern1 = '\d{4}\D\d+\D\d+\s\d+:\d+:\d+'
            #time = re.match(pattern1, article.content)
    
            # 存储数据
            sql = "INSERT INTO dizhen2( title, content ) "
            sql = sql + " VALUES ('%s', '%s') "
            data = (article.title, article.content)
            cursor.execute(sql % data)
            connect.commit()
    
        except Exception as e:
            print(e)
            continue
while 1==1:
    # 获取首页链接
    #创建request对象
    url_set = list()  # url集合
    #request = urllib2.Request(home)
    request = urllib.request.Request(home)
    #添加http的header
    request.add_header('User-Agent', 'Mozilla/5.0')
    #发送请求获取结果
    #response = urllib2.urlopen(request)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    #pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'
    #pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+\.html'
    #pattern = 'http://www\.jianzai\.gov\.cn//DRpublish/ywcp/\d+'
    pattern = '/publish/dizhenj/464/479/\d+/index\.html'
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
            if url not in url_old:
                # 获取代码
                html1 = urllib.request.urlopen(url)
                html = html1.read().decode('utf-8')
        
                # DOM解析
                soup = bs4.BeautifulSoup(html, 'html.parser')
                article = Article()
                page1 = soup.find('div', {'class': 'detail_main_right_conbg_tit'})
                page2 = soup.find('div', {'class': 'detail_main_right_conbg_con'})
                article.title = page1.find('div', {'style': "text-align:center;font-size:24px;padding-top:5px 0;font-weight:bolder;font-family:'黑体';"}).get_text()
                article.content = page2.find('div', {'style': 'font-size:16px;'}).get_text()
                # 将正则表达式编译成Pattern对象
                #时间
                pattern1 = re.compile(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}')
                #地点
                pattern2 = re.compile(r'分(.+)发')
                pattern3 = re.compile(r'\d+\.\d+')
                # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
                mat1 = re.search(pattern1,article.content)
                time1 = mat1.group(0)
                mat2 = re.search(pattern2,article.title)
                #mat2 = re.search(pattern2,article.title.encode('utf-8'))
                location = mat2.group(1)
                #location = unicode(mat2.group(1), "utf-8")
                mat3 = re.findall(pattern3,article.content)
                zhenji = mat3[0]
                latitude = mat3[1]
                longitude = mat3[2]
                depth = mat3[4]
                sql = "INSERT INTO dizhenparse2( time, location, zhenji, latitude, longtitude, depth ) "
                sql = sql + " VALUES ('%s', '%s', '%s', '%s', '%s', '%s') "
                data = (time1, location, zhenji, latitude, longitude, depth)
                cursor.execute(sql % data)
                connect.commit()
                #print mat1.group(0)
                #print mat2.group(1)
                #pattern1 = '\d{4}\D\d+\D\d+\s\d+:\d+:\d+'
                #time = re.match(pattern1, article.content)
        
                # 存储数据
                sql = "INSERT INTO dizhen2( title, content ) "
                sql = sql + " VALUES ('%s', '%s') "
                data = (article.title, article.content)
                cursor.execute(sql % data)
                connect.commit()
                url_old.add(url)
    
        except Exception as e:
            print(e)
            continue
    time.sleep(interval)
# 关闭数据库连接
cursor.close()
connect.close()
'''
Created on 2017年12月28日

@author: liuwei
'''
