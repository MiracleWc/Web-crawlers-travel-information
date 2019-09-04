import requests
import pymysql
from bs4 import BeautifulSoup
db = pymysql.connect("localhost", "root", "205814", "travel")
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianView")
sql21 = """CREATE TABLE travel.xianView (
         id int not null primary key auto_increment,
         viewPort text(100) CHARACTER SET utf8 ,
         content text(100) CHARACTER SET utf8,
         source text(100) CHARACTER SET utf8,
         comment text(100) CHARACTER SET utf8,
         image text(200) CHARACTER SET utf8)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianView(viewPort,content,source,comment,image) 
        VALUES(%s,%s,%s,%s,%s)"""
# 关闭数据库连接
for i in range(1, 4):
    url = requests.get('https://travel.qunar.com/p-cs300100-xian-jingdian-1-'+str(i))  # 请求这个网址
    soup = BeautifulSoup(url.content, "lxml")  # 解析网址
# print(soup)  #可以查看HTML源代码
    for j in range(1, 11):
        viewPorts = soup.select('ul > li:nth-child('+str(j)+') > div > div.titbox.clrfix > a > span.cn_tit')
        viewPort2s = soup.select('li:nth-child(' + str(j) + ')>div>div.titbox.clrfix >a>span>span.en_tit')
        contents = soup.select('div.listbox > ul > li:nth-child('+str(j)+') > div > div.txtbox.clrfix > div.desbox')
        images = soup.select('div.qn_main_ct_l > div > div.listbox > ul > li:nth-child('+str(j)+') > a > img')
        comments = soup.select('li:nth-child('+str(j)+') > div > div.txtbox.clrfix > div.countbox > span.ranking_sum')

        for viewPort, viewPort2, content, image, comment in \
                zip(viewPorts, viewPort2s, contents, images, comments):
            da = {
                 'viewPort1': viewPort.get_text().strip(viewPort2.get_text()),
                 'content': content.get_text(),
                 'source': 'qunar',
                 'comment': comment.get_text(),
                 'img': image.get('src')
             }
            dat = (viewPort.get_text().strip(viewPort2.get_text()), content.get_text(), 'qunar', comment.get_text(),
                   image.get('src'))
            print(da)  # 遍历列表，并用字典存储
            cursor.execute(sql22, dat)
            db.commit()

cursor.close()
db.close()