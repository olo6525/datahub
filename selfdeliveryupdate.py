import json
import os
from smtpd import Options
from time import sleep
import pymysql
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import shutil
import requests

db=pymysql.connect(user='user_me', passwd='Qordnjsrldustmq1!', host='3.36.86.210', db='storedb', charset='utf8')
curs = db.cursor()
url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
params = "query=" + "경기도 시흥시 은계번영길 7(단디프라자 1층 102호 은행동)" + "&X-NCP-APIGW-API-KEY-ID=kvk4abf4qy&X-NCP-APIGW-API-KEY=24zN4WAXOvTx96sUImiKnYAFX2K8KRES8sYPEIC0"
res = requests.get(url, params)
storename = ""
storeaddress = ""
storelocation = ""
storenum = ""
location = json.loads(res.text)
latitude = float(0)
longitude = float(0)
try:
    location = location['addresses'][0]
    latitude = float(location['y'])
    longitude = float(location['x'])
    print(latitude)
    print(longitude)
except Exception:
    pass
    print('주소없음')
sql = "insert selfdeliverystore into (storename, storeaddress, storelocation, storenum, latitude, longitude) values (%s, %s, %s, %s, %s, %s)"
val = (
    storename, storeaddress, storelocation, storenum, float(latitude), float(longitude)
)
curs.execute(sql, val)
db.commit()

db.close()
driver.close()





