
#アルファベットと文字列を対応させる関数を作成
#http://qiita.com/fumitoh/items/d70c6dfbd35a053a5706
def column_index(name):
    import string
    index = string.ascii_uppercase.index
    column = 0
    for c in name.upper():
        column = column * 26 + index(c) + 1
    return column

import bs4, re, sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from sources import std_data


import logging
logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('START')

def login(browser='Firefox'):

    # ブラウザを選択
    if browser == 'Firefox':
        driver = webdriver.Firefox(executable_path=r'C:\autoDownload\sources\geckodriver.exe')
    elif browser == 'PhantomJS':
        driver = webdriver.PhantomJS()
    elif browser == 'Chrome':
        driver = webdriver.Chrome(executable_path=r'C:\autoDownload\sources\chromedriver.exe')
    else:
        print('There is not such a driver')
        driver = webdriver.Firefox()

    wait = WebDriverWait(driver, 10)

    #--------------------ユーザー名とパスワード認証--------------------
    driver.get('https://portal.nap.gsic.titech.ac.jp/GetAccess/Login?Template=userpass_key&AUTHMETHOD=UserPassword')

    name_elem = driver.find_element_by_name('usr_name')
    name_elem.clear()
    name_elem.send_keys(std_data.STUDENT_NUMBER)

    pas_elem = driver.find_element_by_name('usr_password')
    pas_elem.clear()
    pas_elem.send_keys(std_data.STUDENT_PASSWORD)

    pas_elem.submit()
    isUrl = wait.until(expected_conditions.url_contains("https://portal.nap.gsic.titech.ac.jp/GetAccess/Login?Template=idg_key&AUTHMETHOD=IG&GASF=CERTIFICATE,IG.GRID,IG.OTP&LOCALE=ja_JP&GAREASONCODE=13&GAIDENTIFICATIONID=UserPassword&GARESOURCEID=resourcelistID2&GAURI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList&Reason=13&APPID=resourcelistID2&URI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList"))
    logging.debug(isUrl)

    #-------------------マトリクス認証----------------------
    # マトリクス座標を表す文字列に対応する正規表現を作成
    # '[' + 'capital' + ',' + 'number'  + ']'
    coordinate_regex = re.compile(r'\[([A-Z]),(\d)\]')

    # すべてのth要素のテキストからマトリクスの座標を表現する文字列を探す
    soup = bs4.BeautifulSoup(driver.page_source, "lxml")
    elems = soup.select('th')
    points = []
    for i in range(len(elems) - 1):
        logging.debug('{} : {}'.format(i, elems[i]))
        coordinate = elems[i].getText()
        mo = coordinate_regex.search(coordinate)
        if mo:
            capital = mo.group(1)
            number = mo.group(2)
            x = column_index(capital) - 1
            y = int(number) - 1
            points.append([x, y])

    mpas_elems = driver.find_elements_by_css_selector('input[type="password"]')

    for elem in mpas_elems:
        i = mpas_elems.index(elem)
        elem.clear()
        elem.send_keys(std_data.MATRIX[points[i][0]][points[i][1]])

    mpas_elems[0].submit()

    isUrl = wait.until(expected_conditions.url_contains("https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList"))
    logging.debug(isUrl)
    if not __name__ == "__main__":
        return driver


if __name__ == "__main__":
    if len(sys.argv) < 2:
        login()

    else:
        login(sys.argv[1])
