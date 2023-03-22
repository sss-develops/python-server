#제목: 네이버 검색 API 활용하기

import urllib.request
import sys, json
from search2 import search, insert
import pymysql
import schedule
import time

# pip install schedule, pymysql, requests

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client_id = "[자신의 client id]"
    client_secret = "[자신의 client secret]"


    insert("금융", client_id, client_secret)
    #schedule.every(1).seconds.do(insert, "금융", client_id, client_secret)
    #schedule.every().day.at("17:10").do(insert, "금융", client_id, client_secret)
    schedule.every(8).hours.do(insert,"금융",client_id,client_secret)

    count = 0

    while True:
        schedule.run_pending()
        #count += 1
        #time.sleep(1)
        #print(count)