import requests
import urllib.request as urllib2
import json
import pymysql
from bs4 import BeautifulSoup
import re
import datetime
starttime = datetime.datetime.now()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}
pattern = re.compile(r'\d+')
db = pymysql.connect("localhost", "root", "205814", "travel")
cursor = db.cursor()
# 创建数据表SQL语句
cursor.execute("DROP TABLE IF EXISTS travel.xianViewQunar")
sql21 = """CREATE TABLE travel.xianViewQunar (
         id int not null primary key auto_increment,
         viewPort text(100) CHARACTER SET utf8 ,
         viewPortEn text(100) CHARACTER SET utf8 ,
         point float,
         allNum int,
         goodNum int,
         content text(100) CHARACTER SET utf8 ,
         image text(100) CHARACTER SET utf8 ,
         comment text(100) CHARACTER SET utf8 ,
         detail text(100) CHARACTER SET utf8,       
         openTime text(100) CHARACTER SET utf8,
         img1 text(200) CHARACTER SET utf8,
         img2 text(200) CHARACTER SET utf8,
         img3 text(200) CHARACTER SET utf8,
         img4 text(200) CHARACTER SET utf8,
         img5 text(200) CHARACTER SET utf8,
         ticket1 text(100) CHARACTER SET utf8,
         price1 float,
         ticket2 text(100) CHARACTER SET utf8,
         price2 float)"""
cursor.execute(sql21)
sql22 = """INSERT INTO travel.xianViewQunar(viewPort,viewPortEn,point,allNum,goodNum,content,image,comment,detail,
openTime,img1,img2,img3,img4,img5,ticket1,price1,ticket2,price2) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
# 关闭数据库连接
for i in range(1, 5):
    url = requests.get('https://travel.qunar.com/p-cs300100-xian-jingdian-1-'+str(i))  # 请求这个网址
    soup = BeautifulSoup(url.content, "lxml")  # 解析网址
# print(soup)  #可以查看HTML源代码
    for j in range(1, 11):
        url_indexs = soup.select('div.qn_main_ct_l > div > div.listbox > ul > li:nth-child('+str(j)+') > a')

        contents = soup.select('div.listbox > ul > li:nth-child(' + str(j) + ') > div > div.txtbox.clrfix > div.desbox')
        images = soup.select('div.qn_main_ct_l > div > div.listbox > ul > li:nth-child(' + str(j) + ') > a > img')
        comments = soup.select(
            'li:nth-child(' + str(j) + ') > div > div.txtbox.clrfix > div.countbox > span.ranking_sum')
        for url_index, content, image, comment in zip(url_indexs, contents, images, comments):
            content_s = content.get_text()
            comment_s = comment.get_text()
            image_s = image.get('src')
            url_index_s = url_index.get('href')
            print(url_index_s)
            url_next = requests.get(url_index_s)  # 请求这个网址
            soup_next = BeautifulSoup(url_next.content, "lxml")  # 解析网址

            viewPorts = soup_next.select('div.b_title.clrfix > h1')
            viewPortEns = soup_next.select('div.b_title.clrfix > h1 > span')
            img1s = soup_next.select('li:nth-child(1) > div.imgbox > img')
            img2s = soup_next.select('li:nth-child(2) > div.imgbox > img')
            img3s = soup_next.select('li:nth-child(3) > div.imgbox > img')
            img4s = soup_next.select('li:nth-child(4) > div.imgbox > img')
            img5s = soup_next.select('li:nth-child(5) > div.imgbox > img')
            ticket1s = soup_next.select(' div.e_ticket_info_box > div.e_ticket_info > dl:nth-child(1) > dt')
            price1s = soup_next.select(' div.e_ticket_info > dl:nth-child(1) > dd.e_now_price > span')

            ticket2s = soup_next.select(' div.e_ticket_info_box > div.e_ticket_info > dl:nth-child(2) > dt')
            price2s = soup_next.select(' div.e_ticket_info > dl:nth-child(2) > dd.e_now_price > span')

            url_index2s = soup_next.select('div.e_ticket_info_box > div.e_ticket_info > dl:nth-child(2) > dd.e_view_price_box > a')
            for url_index2 in url_index2s:
                url_index2_s = url_index2.get('href')
                print(url_index2_s)

                str_s = pattern.findall(url_index2_s)
                for str_ss in str_s:
                    print(str_ss)
                    tag = str_ss
                url = 'https://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId='+tag+'&index=1&page=1&pageSize=10&tagType=0'
                req = urllib2.Request(url, headers=headers)
                response = urllib2.urlopen(req).read().decode()
                json_dict = json.loads(response)
                point = json_dict["data"]["score"]
                allNum = json_dict["data"]["tagList"][0]["tagNum"]
                goodNum = json_dict["data"]["tagList"][1]["tagNum"]
                print(point)

                url2_next = requests.get(url_index2_s)  # 请求这个网址
                soup2_next = BeautifulSoup(url2_next.content, "lxml")  # 解析网址
                details = soup2_next.select('#mp-charact > div:nth-child(1) > div.mp-charact-intro > div.mp-charact-desc > p')
                openTimes = soup2_next.select('#mp-charact > div:nth-child(1) > div.mp-charact-time > div > div.mp-charact-desc > p')
                for viewPort, viewPortEn, detail, openTime, img1, img2, img3, img4, img5, ticket1, price1, ticket2, price2 \
                        in zip(viewPorts, viewPortEns, details, openTimes, img1s, img2s, img3s,
                               img4s, img5s, ticket1s, price1s, ticket2s, price2s):
                    dat = (viewPort.get_text().strip(viewPortEn.get_text()), viewPortEn.get_text(), point, allNum,
                           goodNum, content_s, image_s, comment_s, detail.get_text(), openTime.get_text(), img1.get('src'),
                           img2.get('src'), img3.get('src'), img4.get('src'), img5.get('src'), ticket1.get_text(),
                           float(price1.get_text().strip('¥')), ticket2.get_text(), float(price2.get_text().strip('¥')))
                    print(dat)  # 遍历列表，并用字典存储
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