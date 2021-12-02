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

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(time_to_wait=5)
driver.get(url='http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813#page1')
driver.implicitly_wait(time_to_wait=1)
check_box = driver.find_element_by_xpath('//*[@id="mode1"]/div[1]/div[1]/ul/li[4]/a')
check_box.click()
driver.implicitly_wait(time_to_wait=5)
close_popup_button = driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[2]/a[2]')
close_popup_button.click()
driver.implicitly_wait(time_to_wait=2)
search_button = driver.find_element_by_xpath('//*[@id="srchBtn"]')
sleep(2)
search_button.click()
sleep(10)
howmanylist_button=driver.find_element_by_xpath('//*[@id="a_list_cnt"]')
howmanylist_button.click()
find50list_button=driver.find_element_by_xpath('//*[@id="contents"]/main/section/div[2]/div[2]/div[3]/div/ul/li[5]/a')
find50list_button.click()
sleep(3)

for i in range(2, 93655):
    driver.get(
        url='http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813#page' + str(
            i))
    print(str(i))
    while True:
        try:
            lodingicon = driver.find_element_by_xpath('//*[@id="fancybox-loading"]')
            sleep(2)
            print('wait')
        except:
            print('now get data')
            for j in range(1, 51):
                store_num = driver.find_element_by_xpath('//*[@id="tbl_bsn_list"]/tbody/tr[' + str(j) + ']/td[2]')
                store_name = driver.find_element_by_xpath('//*[@id="tbl_bsn_list"]/tbody/tr[' + str(j) + ']/td[3]')
                store_address = driver.find_element_by_xpath('//*[@id="tbl_bsn_list"]/tbody/tr[' + str(j) + ']/td[6]')
                store_city = driver.find_element_by_xpath('//*[@id="tbl_bsn_list"]/tbody/tr[' + str(j) + ']/td[7]')
                url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
                address = store_address.text
                params = "query=" + address + "&X-NCP-APIGW-API-KEY-ID=kvk4abf4qy&X-NCP-APIGW-API-KEY=24zN4WAXOvTx96sUImiKnYAFX2K8KRES8sYPEIC0"
                res = requests.get(url, params)
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
                sql = "insert into storeinfo (storenum, storename, storeaddress, storelocation, latitude, longitude) values(%s, %s, %s, %s, %s, %s) on duplicate key update latitude=%s, longitude=%s"
                val = (
                store_num.text, store_name.text, store_address.text, store_city.text, float(latitude), float(longitude),
                float(latitude), float(longitude))
                curs.execute(sql, val)
                db.commit()
            break

db.close()
driver.close()





