#! python
# autodownload.py - OCW-iから講義資料をダウンロードし、GDriveにアップロード

# デバッグ用
import logging
logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('START')
# -------------------------------------------------------------------------------------------

from sources import G_uploader
import requests, bs4, re, os, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from sources import login
print(os.getcwd()) # debug
time.sleep(2.0) # debug
print("portalにログインしています…")
driver = login.login('PhantomJS')
wait = WebDriverWait(driver, 10)

def moveToUrl(driver, url):
    driver.get(url)
    isUrl = wait.until(expected_conditions.url_contains(url))
    logging.debug('move to '+ url)
    return isUrl

print("講義情報を取得しています…")
# OCW-iにページ遷移
ocwi_url = 'https://secure.ocw.titech.ac.jp/ocwi/index.php'
moveToUrl(driver, ocwi_url)

# 受講講義一覧にページ遷移
lectureList_url = 'https://secure.ocw.titech.ac.jp/ocwi/index.php?module=Ocwi&action=LectureList'
moveToUrl(driver, lectureList_url)

# 講義番号から講義ノートのページのURLを作成

lectureNum_selecter = 'input[type="hidden"]'
lectureNum_elems = driver.find_elements_by_css_selector(lectureNum_selecter)
logging.debug(len(lectureNum_elems))

lectureList_url_list = []
for elem in lectureNum_elems:
    valString = elem.get_attribute("value")
    logging.debug(valString)
    lectureNote_url = 'https://secure.ocw.titech.ac.jp/ocwi/index.php?module=Ocwi&action=KougiNote&JWC=' + valString
    logging.debug(lectureNote_url)
    lectureList_url_list.append(lectureNote_url)

# cookieの受け渡し
session = requests.session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

# ダウンロードされたファイルを数える
file_counter = 0

# 講義ノートのページに移動し、資料をダウンロード
title_selector = '#lectureTtl > h1'
for url in lectureList_url_list:
    # ページ移動
    moveToUrl(driver, url)

    # 講義タイトルを作成
    title_elem = driver.find_element_by_css_selector(title_selector)
    class_title = title_elem.text
    class_title = class_title.split('\n')[0]
    logging.debug(class_title)
    print("{}の講義資料を検索しています…".format(class_title))

    # 講義資料を保存するフォルダを作成
    dirpath = os.path.join(r'C:\Users\eita6\Documents\LectureDoc',class_title)
    exists_file = driver.find_elements_by_class_name("file")
    if exists_file:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    lectureNote_elems = driver.find_elements_by_xpath('//*[@class="lectureNote clearfix"]')
    for lectureNote_elem in lectureNote_elems:
        # 授業のタイトルを作成
        lectureTitle_elem = lectureNote_elem.find_element_by_xpath('.//h2/div')
        lecture_title = lectureTitle_elem.text
        logging.debug('lecture_title = ', lecture_title)

        # 講義資料ファイルの要素を指定
        file_elems = lectureNote_elem.find_elements_by_xpath('.//ul[2]/li/a')
        logging.debug(lecture_title, 'len(file_elems) = ', str(len(file_elems)))
        if file_elems:
            for num, file_elem in enumerate(file_elems, 1):
                # 保存時のファイル名を作成
                doc_url = file_elem.get_attribute('href')
                logging.debug(doc_url)
                extention = '.' + doc_url.split('&JWC=')[0].split('.')[-1]
                filename = lecture_title + str(num) + extention
                doc_file_path = os.path.join(dirpath, filename)
                # ファイルのダウンロード
                if not os.path.exists(doc_file_path):
                    file_counter += 1
                    print("{}をダウンロードしています…".format(filename))
                    res = session.get(doc_url)
                    res.raise_for_status()
                    doc_file = open(doc_file_path, 'wb')
                    for chunk in res.iter_content(100000):
                        doc_file.write(chunk)
                    doc_file.close()
                    # ファイルをGDriveにアップロード
                    print("{}をGDriveにアップロードしています…".format(filename))
                    G_uploader.G_upload(doc_file_path)


driver.close()
print('{}個のファイルをダウンロードしました'.format(file_counter))
