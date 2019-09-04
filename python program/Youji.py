import urllib.request as urllib2
import json
import pymysql
db = pymysql.connect("localhost", "root", ***, "travel")   # ***means password of your MySQL Database
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianYouji")
sql21 = """CREATE TABLE travel.xianYouji(
         id int not null primary key auto_increment,
         name text(100) CHARACTER SET utf8 ,
         summary text(100) CHARACTER SET utf8,
         time text(100) CHARACTER SET utf8,
         picUrl text(100) CHARACTER SET utf8,
         authorName text(200) CHARACTER SET utf8,
         address text(200) CHARACTER SET utf8,
         source text(200) CHARACTER SET utf8)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianYouji(name,summary,time,picUrl,authorName,address,source)
        VALUES(%s,%s,%s,%s,%s,%s,%s)"""
# 关闭数据库连接
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
for i in range(1, 4):
    url = 'http://trips.tuniu.com/travels/index/ajax-list?queryKey=%E8%A5%BF%E5%AE%89&page='+str(i)+'&limit=10&_=1554868683607'
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req).read().decode()
    json_dict = json.loads(response)
    for j in range(0, 10):
        name = json_dict["data"]["rows"][j]["name"]
        summary = json_dict["data"]["rows"][j]["summary"]
        time = json_dict["data"]["rows"][j]["publishTime"]
        picUrl = json_dict["data"]["rows"][j]["picUrl"]
        authorName = json_dict["data"]["rows"][j]["authorName"]
        dat = (name, summary, time, picUrl, authorName, '西安', '途牛')
        print(dat)
        cursor.execute(sql22, dat)
        db.commit()
cursor.close()
db.close()
