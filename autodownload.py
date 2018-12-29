#! python
# autodownload.py - OCW-iから講義資料をダウンロードし、GDriveにアップロード

# デバッグ用
import logging
logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('START')
# -------------------------------------------------------------------------------------------

from sources import G_functions

import requests, bs4, re, os, time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from sources import login
import pickle

print("portalにログインしています…")
driver = login.login('PhantomJS')
wait = WebDriverWait(driver, 10)

def moveToUrl(driver, url):
    driver.get(url)
    isUrl = wait.until(expected_conditions.url_contains(url))
    return isUrl

# 講義資料情報を保存するフォルダが無ければ新規作成
if not os.path.exists('lectureDocs.pickle'):
    with open('lectureDocs.pickle', mode='wb') as f:
        pickle.dump([], f)

if not os.path.exists('courses.pickle'):
    with open('courses.pickle', mode='wb') as f:
        pickle.dump([], f)

# フォルダから講義資料情報を取り出す
with open('lectureDocs.pickle', mode='rb') as f:
    lectureDocs = pickle.load(f)

with open('courses.pickle', mode='rb') as f:
    courses = pickle.load(f)


# OCW-iにページ遷移
print("講義情報を取得しています…")
ocwi_url = 'https://secure.ocw.titech.ac.jp/ocwi/index.php'
moveToUrl(driver, ocwi_url)

# 受講講義一覧にページ遷移
lectureList_url = 'https://secure.ocw.titech.ac.jp/ocwi/index.php?module=Ocwi&action=LectureList'
moveToUrl(driver, lectureList_url)

lecture_selecter = '.contents > table:nth-child(n) > tbody:nth-child(1) > tr:nth-child(n) > td:nth-child(1) > a:nth-child(1)'
lectureLinkElems = driver.find_elements_by_css_selector(lecture_selecter)

# 講義情報一覧の作成
courses = []
for elem in lectureLinkElems:
    course = G_functions.Course(title=elem.text, link=elem.get_attribute("href"))
    courses.append(course)

# cookieの受け渡し
session = requests.session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

# ダウンロードされたファイルを数える
file_counter = 0

# 講義ノートのページに移動し、資料をダウンロード
title_selector = '#lectureTtl > h1'
for course in courses:
    moveToUrl(driver, course.link)
    print("{}の講義資料を検索しています…".format(course.title))

    # 講義資料を保存するフォルダを作成
    dirpath = os.path.join(r'C:\Users\eita6\Documents\LectureDoc',course.title)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    # 講義の各授業を探索
    lectureNote_elems = driver.find_elements_by_xpath('//*[@class="lectureNote clearfix"]')
    for lectureNote_elem in lectureNote_elems:
        # 授業のタイトルを作成
        lectureTitle_elem = lectureNote_elem.find_element_by_xpath('.//h2/div')
        lecture_title = lectureTitle_elem.text

        # 講義資料ファイルの要素を指定
        file_elems = lectureNote_elem.find_elements_by_xpath('.//ul[2]/li/a')
        if file_elems:
            for num, file_elem in enumerate(file_elems, 1):
                # 保存時のファイル名を作成
                doc_url = file_elem.get_attribute('href')
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

                    # lectureインスタンスを作成
                    lectureDoc = G_functions.LectureDoc(path=doc_file_path, course=course)
                    lectureDocs.append(lectureDoc)

                    # ファイルをGDriveにアップロード
                    print("{}をGDriveにアップロードしています…".format(lectureDoc.title))
                    lectureDoc.upload()

driver.close()

# 講義と授業の情報を保存
with open('lectureDoc.pickle', mode='wb') as f:
    pickle.dump(lectureDocs, f)
with open('courses.pickle', mode='wb') as f:
    pickle.dump(courses, f)

print('{}個のファイルをダウンロードしました'.format(file_counter))
