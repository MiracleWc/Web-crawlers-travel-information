import requests
import pymysql
from bs4 import BeautifulSoup
import datetime
starttime = datetime.datetime.now()
db = pymysql.connect("localhost", "root", "205814", "travel")
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianPlay")
sql21 = """CREATE TABLE travel.xianPlay(
         id int not null primary key auto_increment,
         playName text(100) CHARACTER SET utf8 ,
         money text(100) CHARACTER SET utf8,
         address text(100) CHARACTER SET utf8,
         comment text(100) CHARACTER SET utf8,
         image text(200) CHARACTER SET utf8)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianPlay(playName,money,address,comment,image) 
        VALUES(%s,%s,%s,%s,%s)"""
# 关闭数据库连接
for i in range(1, 4):
    url = requests.get('https://travel.qunar.com/p-cs300100-xian-wanle?page='+str(i))  # 请求这个网址
    soup = BeautifulSoup(url.content, "lxml")  # 解析网址
# print(soup)  #可以查看HTML源代码
    for j in range(1, 11):
        playNames = soup.select('ul > li:nth-child('+str(j)+') > div > div.titbox.clrfix > a > span')
        moneys = soup.select('ul > li:nth-child('+str(j)+') > div > div.sublistbox > dl:nth-child(1) > dd')
        addresses = soup.select('ul > li:nth-child('+str(j)+') > div > div.sublistbox > dl > dd')
        comments = soup.select('li:nth-child(' + str(j) + ') > div > div.sublistbox > div > span.txt')
        images = soup.select('div.qn_main_ct_l > div > div.listbox > ul > li:nth-child('+str(j)+') > a > img')
        for playName, money, address, comment, image in zip(playNames, moneys, addresses, comments, images):
            da = {
                 'playName': playName.get_text(),
                 'money': money.get_text(),
                 'address': address.get_text(),
                 'comment': comment.get_text(),
                 'image': image.get('src')
             }
            dat = (playName.get_text(), money.get_text(), address.get_text(), comment.get_text(), image.get('src'))
            print(da)  # 遍历列表，并用字典存储
            cursor.execute(sql22, dat)
            db.commit()
cursor.close()
db.close()
endtime = datetime.datetime.now()
print(endtime - starttime)