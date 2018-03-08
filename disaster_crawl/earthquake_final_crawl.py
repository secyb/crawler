import pymysql  # 数据库连接模块
import bs4  # DOM解析模块
import json
import urllib.request
import re
import time

eq_url = 'http://hisz.rsoe.hu/alertmap/database/mapData/eq.json'

def sleeptime(hour,minute,sec):
    return hour*3600 + minute*60 + sec
interval = sleeptime(1,0,0);

# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '123456',
    'database': 'disater',
    'charset': 'utf8'
}

# 地震事件定义类
class EarthquakeEvents(object):
    def __init__(self):
        self.number = None
        self.magnitude = None
        self.mercalliscale = None
        self.datetime1 = None
        self.localtime1 = None
        self.coordinate = None
        self.depth = None
        self.hypocentrum = None
        self.classtype = None
        self.continent = None
        self.country = None
        self.location = None
        self.source = None
        self.potentialimpact = None


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

# 得到json字典
def get_dic(url):
    #创建request对象
    request = urllib.request.Request(url)
    #添加http的header
    request.add_header('User-Agent', 'Mozilla/5.0')
    #发送请求获取结果
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    response.close()
    dic=json.loads(html)
    return dic

url_old = set()  # 过期url

while 1==1:
    rid_set = set()
    # 爬取地震事件数据
    value = get_dic(eq_url)
    subvalue = value['data']
    for subkey in subvalue:
        item = subkey['rid']
        rid_set.add(item)
      
    url_set = set()
    
    #print len(url_set)
    for item in rid_set:
        url = "http://hisz.rsoe.hu/alertmap/database/index.php?pageid=seism_index&" + "rid=" + item
        url_set.add(url)
    
    #for url in url_set:';
    #    print url
    
    while len(url_set) != 0:
        try:
            # 获取链接
            url = url_set.pop()
            
            if url not in url_old:
                # 获取代码
                html1 = urllib.request.urlopen(url)
                html = html1.read().decode('utf-8')
        
                # DOM解析
                soup = bs4.BeautifulSoup(html, 'html.parser') 
                earthquakeevents = EarthquakeEvents()
                tables = soup.find_all('table')
                #for table in tables:
                #    print table
                if len(tables)!=0:
                    tab = tables[0]
                    #print tab
                    data_list = list()
                    for tr in tab.findAll('tr'):  
                        for td in tr.findAll('td'):  
                            data_list.append(td.getText()) 
                    earthquakeevents.number = data_list[0]
                    earthquakeevents.magnitude = data_list[1]
                    earthquakeevents.mercalliscale = data_list[2]
                    earthquakeevents.datetime1 = data_list[3]
                    earthquakeevents.localtime1 = data_list[4]
                    earthquakeevents.coordinate = data_list[5]
                    earthquakeevents.depth = data_list[6]
                    earthquakeevents.hypocentrum = data_list[7]
                    earthquakeevents.classtype = data_list[8]
                    earthquakeevents.continent = data_list[9]
                    earthquakeevents.country = data_list[10]
                    earthquakeevents.location = data_list[11].replace('\n','')
                    earthquakeevents.source = data_list[12]
                    earthquakeevents.potentialimpact = data_list[13].replace('\n','')
                    pattern1 = re.compile(r'\d.*')
                    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
                    mat1 = re.search(pattern1,earthquakeevents.location)
                    earthquakeevents.location = mat1.group(0)
                    pattern2 = re.compile(r'\w.*')
                    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
                    mat2 = re.search(pattern2,earthquakeevents.potentialimpact)
                    earthquakeevents.potentialimpact = mat2.group(0)
                    
                    a = earthquakeevents.coordinate.split(',')[0]
                    #print (a.split('°'))
                    b = float(a.split('°')[1][1:])/60
                    c = a.split('°')[0]
                    d = float(c)+b
                    latitude = str(d)
                    e = earthquakeevents.coordinate.split(',')[1]
                    #print (a.split('°'))
                    f = float(e.split('°')[1][1:])/60
                    g = e.split('°')[0]
                    h = float(g)+f
                    longtitude = str(h)
                    
                    # 存储数据
                    sql = "INSERT INTO earthquake2( number, magnitude, mercalliscale, datetime1, localtime1, latitude, longtitude, depth, hypocentrum, classtype, continent, country, location, source, potentialimpact ) "
                    sql = sql + " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') "
                    data = (earthquakeevents.number, earthquakeevents.magnitude, earthquakeevents.mercalliscale, earthquakeevents.datetime1, earthquakeevents.localtime1
                            , latitude, longtitude, earthquakeevents.depth, earthquakeevents.hypocentrum, earthquakeevents.classtype, earthquakeevents.continent,
                            earthquakeevents.country, earthquakeevents.location, earthquakeevents.source, earthquakeevents.potentialimpact)
                    cursor.execute(sql % data)
                    connect.commit()
                    url_old.add(url)
            time.sleep(10)
            
                
    
        except Exception as e:
            print(e)
            continue
    time.sleep(interval)
#f.close()
# 关闭数据库连接
cursor.close()
connect.close()
'''
Created on 2017年12月28日

@author: liuwei
'''
