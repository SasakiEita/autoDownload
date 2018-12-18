#! python

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

G_uploader.G_listFiles()
