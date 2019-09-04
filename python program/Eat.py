import requests
import pymysql
import re
from bs4 import BeautifulSoup
import datetime
starttime = datetime.datetime.now()
pattern = re.compile(r'\d+')
db = pymysql.connect("localhost", "root", "205814", "travel")
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianEat")
sql21 = """CREATE TABLE travel.xianEat(
         id int not null primary key auto_increment,
         eatName text(100) CHARACTER SET utf8 ,
         money int ,
         point float,
         foodName text(100) CHARACTER SET utf8 ,
         address text(100) CHARACTER SET utf8,
         comment text(100) CHARACTER SET utf8,
         image text(200) CHARACTER SET utf8)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianEat(eatName,money,point,foodName,address,comment,image) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)"""
# 关闭数据库连接
for i in range(1, 4):
    url = requests.get('https://travel.qunar.com/p-cs300100-xian-meishi?page='+str(i))  # 请求这个网址
    soup = BeautifulSoup(url.content, "lxml")  # 解析网址
# print(soup)  #可以查看HTML源代码
    for j in range(1, 11):
        eatNames = soup.select('ul > li:nth-child('+str(j)+') > div > div.titbox.clrfix > a > span')
        moneys = soup.select('ul > li:nth-child('+str(j)+') > div > div.sublistbox > dl:nth-child(1) > dd')
        foodNames = soup.select(' ul > li:nth-child('+str(j)+') > div > div.sublistbox > dl:nth-child(3) > dd')
        addresses = soup.select('ul > li:nth-child(' + str(j) + ') > div > div.sublistbox > dl:nth-child(2) > dd')
        comments = soup.select('li:nth-child(' + str(j) + ') > div > div.sublistbox > div > span.txt')
        images = soup.select('div.qn_main_ct_l > div > div.listbox > ul > li:nth-child('+str(j)+') > a > img')
        points = soup.select(' ul > li:nth-child(' + str(j) + ') > div > div.titbox.clrfix > div > div > span.cur_score')
        for eatName, money,point, foodName, address, comment, image in \
                zip(eatNames, moneys, points, foodNames, addresses, comments, images):
            money_s = pattern.findall(money.get_text())
            da = {
                'eatName': eatName.get_text(),
                'money': money_s[0],
                'point': point.get_text(),
                'foodName': foodName.get_text(),
                'address': address.get_text(),
                'comment': comment.get_text(),
                'image': image.get('src')
             }

            dat = (eatName.get_text(), int(money_s[0]), float(point.get_text()), foodName.get_text(), address.get_text(), comment.get_text(),
                   image.get('src'))
            print(da)  # 遍历列表，并用字典存储
            cursor.execute(sql22, dat)
            db.commit()

cursor.close()
db.close()
endtime = datetime.datetime.now()
print(starttime)
print(endtime)
print(endtime - starttime)
time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
print(time_now)