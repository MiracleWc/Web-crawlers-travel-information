import requests
import pymysql
from bs4 import BeautifulSoup
db = pymysql.connect("localhost", "root", ***, "travel")   # ***means password of your MySQL Database
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianXingcheng")
sql21 = """CREATE TABLE travel.xianXingcheng (
         id int not null primary key auto_increment,
         title text(100) CHARACTER SET utf8 ,
         content text(100) CHARACTER SET utf8,
         money text(100) CHARACTER SET utf8,
         address text(100) CHARACTER SET utf8,
         view text(100) CHARACTER SET utf8,
         image text(200) CHARACTER SET utf8)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianXingcheng(title,content,money,address,view,image) 
        VALUES(%s,%s,%s,%s,%s,%s)"""
url = requests.get('http://s.tuniu.com/search_complex/whole-xa-0-%E8%A5%BF%E5%AE%89/1')  # 请求这个网址
soup = BeautifulSoup(url.content, "lxml")  # 解析网址
# print(soup)  #可以查看HTML源代码
for j in range(1, 16):
    titles = soup.select('li:nth-child(' + str(j) + ') > div > a > dl > dt > p.title > span > span.f_0053aa')
    contents = soup.select('li:nth-child(' + str(j) + ') > div > a > dl > dt > p.title > span')
    moneys = soup.select('li:nth-child(' + str(j) + ') > div > a > div.priceinfo > div.tnPrice > em')
    images = soup.select('li:nth-child(' + str(j) + ') > div > a > div.imgbox > div > img')
    views = soup.select('li:nth-child(' + str(j) + ') > div > a > dl > dd.overview > span.overview-scenery')
    for title, content, money, image, view in zip(titles, contents, moneys, images, views):
        content = content.get_text().strip('\n')
        content = content.strip("[五一]")
        content = content.strip(title.get_text())
        da = {
            'title': title.get_text(),
            'content': content,
            'money': money.get_text(),
            'address': '西安',
            'view': view.get_text(),
            'img': image.get('data-src')
        }
        dat = (title.get_text(), content, money.get_text(), '西安', view.get_text(), image.get('data-src'))
        print(da)  # 遍历列表，并用字典存储
        cursor.execute(sql22, dat)
        db.commit()
cursor.close()
db.close()
