import re  # 网络连接模块
import bs4  # DOM解析模块
import pymysql  # 数据库连接模块
import urllib.request  # 网络访问模块
import time

origin_url = 'http://www.creprice.cn/market/distrank/city/wh.html?flag=1&month='
url_home =list()  #初始url集合

for year in range(2014,2017+1):
    for month in range(1,12+1):
        url = origin_url + str(year) + '-' + str(month) + '&type=11'
        url_home.append(url)

for month in range(1,5+1):
    url = origin_url + '2018' + '-' + str(month) + '&type=11'
    url_home.append(url)

# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': '123456',
    'database': 'python',
    'charset': 'utf8'
}

# 文章类定义
class HousePrice(object):
    def __init__(self):
        self.name = None
        self.date = None
        self.category = None
        self.value = None


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
while len(url_home) != 0:
    try:
        # 获取链接
        url = url_home.pop(0)
        pattern1 = re.compile(r'\d{4}-\d+')
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        mat1 = re.search(pattern1,url)
        nian = mat1.group(0).split('-')[0]
        yue = mat1.group(0).split('-')[1]
        shijian = nian +'年'+yue+'月'

        # 获取代码
        html1 = urllib.request.urlopen(url)
        html = html1.read().decode('utf-8')

        # DOM解析
        soup = bs4.BeautifulSoup(html, 'html.parser')
        houseprice = HousePrice()
        tables = soup.find_all('table')
        #for table in tables:
        #    print table
        if len(tables)!=0:
            tab = tables[0]
            data_list = list()
            for tr in tab.findAll('tr'):  
                for td in tr.findAll('td'):  
                    data_list.append(td.getText()) 
        #print(data_list)
        for index in range(0,10):
            houseprice.name = data_list[4*index+1]
            houseprice.date = shijian
            houseprice.category = houseprice.name
            houseprice.value = data_list[4*index+2]
            pattern = re.compile(r'\d+,\d+')
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
            mat = re.search(pattern,houseprice.value)
            #nian = mat.group(0).split(',')[0]
            #yue = mat.group(0).split(',')[1]
            value = mat.group(0).replace(',','')
            # 存储数据
            sql = "INSERT INTO whhouseprice1( name, date, category, value )"
            sql = sql + " VALUES ('%s', '%s', '%s', '%s') "
            data = (houseprice.name, houseprice.date, houseprice.category, value)
            cursor.execute(sql % data)
            connect.commit()
        time.sleep(2)

    except Exception as e:
        print(e)
        continue
    
    
# 关闭数据库连接
cursor.close()
connect.close()
'''
Created on 2018年6月19日

@author: liuwei
'''
