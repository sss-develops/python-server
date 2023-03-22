import pymysql
import urllib.request
import sys, json
import requests
from urllib.parse import quote

def search(string,client_id,client_secret,start_i):

    #search_string = sys.argv[1]
    encText = quote(string)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText +\
          "&display=100" + "&start=" + str(start_i)
    result = requests.get(url=url, headers={"X-Naver-Client-Id":client_id,
    "X-Naver-Client-Secret":client_secret})
    print((result))  # Response [200]
    return result.json()
    # if str(result) == "Response [200]":
    #     return result.json()
    # if (rescode == 200):
    #     response_body = response.read()
    #     #print(response_body.decode('utf-8'))
    #     #print(sys.getsizeof(response_body))
    #     return response.json()
    # else:
    #      print("Error Code:" + result)

def str2datetime(string):
    list = string.split()
    w = list[0][:-1]
    d = list[1]
    b = list[2]
    y = list[3]
    t = list[4]
    # % w % d % b % y % t
    return w,d,b,y,t

def str2datetime2sql(w,d,b,y,t):
    #yyyy - mm - dd
    #hh: mm:ss
    month_list = ["Jan", "Feb", "Mar", "Apr", "May","Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return y+"-"+str(month_list.index(b)+1)+"-"+d+" "+t
   # Fri, 17 Mar 2023    10: 50:00 + 0900
    # % a % d % m % y % t

def str2sql(string):
    print(str2datetime2sql(str2datetime(string)))


def insert(search_keyword,client_id,client_secret):
    db = pymysql.connect(
        host='localhost',  # 접속할 mysql server의 주소
        port=3306,  # 접속할 mysql server의 포트 번호
        user='root',
        passwd='0000',
        db='new_schema',  # 접속할 database명
        charset='utf8'  # 'utf8' 등 문자 인코딩 설정 (한글 데이터가 깨지지 않도록)
    )

    cursor = db.cursor()

    sql4 = "INSERT INTO news (news_title," \
          "original_link," \
          "naver_link," \
          "news_description," \
          "published_at, create_at, last_modified_at) VALUES (%s,%s,%s,%s,%s,%s,%s);"

    sql7 = "SELECT m.original_link" \
           " FROM news AS m" \
           " WHERE m.original_link = %s" \
           " limit 1"
    for start_i in range(1,1000,100):
        data = search(search_keyword, client_id, client_secret, start_i)
        #cursor.execute(sql2, (data["lastBuildDate"], data["total"]))
        w1,d1,b1,y1,t1 = str2datetime(data["lastBuildDate"])
        lastBuildDate = str2datetime2sql(w1,d1,b1,y1,t1)

        # print(str2datetime(data["lastBuildDate"]))
        # print(str2datetime2sql(w1,d1,b1,y1,t1))

        for i in range(100):
            w2,d2,b2,y2,t2 = str2datetime(data["items"][i]["pubDate"])
            pubilished_at = str2datetime2sql(w2, d2, b2, y2, t2)
            #print(cursor.execute(sql7,data["items"][i]["originallink"]))
            if not cursor.execute(sql7,data["items"][i]["originallink"]):
                cursor.execute(sql4,(data["items"][i]["title"],data["items"][i]["originallink"],data["items"][i]["link"],
                                data["items"][i]["description"],pubilished_at,lastBuildDate,lastBuildDate))
    db.commit()
    cursor.close()
    print("is working")