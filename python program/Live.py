import urllib.request as urllib2
import json
import pymysql
import datetime
starttime = datetime.datetime.now()
db = pymysql.connect("localhost", "root", "205814", "travel")
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianLive")
sql21 = """CREATE TABLE travel.xianLive(
         id int not null primary key auto_increment,
         hotelName text(100) CHARACTER SET utf8 ,
         point text(100) CHARACTER SET utf8,
         address text(100) CHARACTER SET utf8,
         picUrl text(100) CHARACTER SET utf8,
         price float,
         source text(200) CHARACTER SET utf8)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianLive(hotelName,point,address,picUrl,price,source)
        VALUES(%s,%s,%s,%s,%s,%s)"""
# 关闭数据库连接
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}
for i in range(1, 3):
    url = 'http://hotel.tuniu.com/ajax/list?search%5Bcity%5D=2702&search%5BcheckInDate%5D=2019-6-20&search%5BcheckOutDate%5D=2019-6-21&search%5BcityCode%5D=2702&page='+str(i)+''
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req).read().decode()
    json_dict = json.loads(response)
    for j in range(0, 19):
        hotelName = json_dict["data"]["list"][j]["name"]
        point = json_dict["data"]["list"][j]["levelInfo"]['name']
        address = json_dict["data"]["list"][j]["addressInfo"]
        picUrl = json_dict["data"]["list"][j]["snapshot"]
        price = json_dict["data"]["list"][j]["startPrice"]
        dat = (hotelName, point, address, picUrl, float(price), '途牛')     # tuple类型
        print(dat)
        cursor.execute(sql22, dat)
        db.commit()
cursor.close()
db.close()
endtime = datetime.datetime.now()
print(starttime)
print(endtime)
print(endtime - starttime)