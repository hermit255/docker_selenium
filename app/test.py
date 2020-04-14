#!/usr/local/bin/python3
# from https://qiita.com/sikkim/items/447b72e6ec45849058cd
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import datetime
import os

# env setting
host = 'selenium-chrome'
wait_default = 1
count_1 = 1

# connection
browser = webdriver.Remote(
    command_executor='http://' + host + ':4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME)

# get datetime for filename
dt = datetime.datetime.today()
dtstr = dt.strftime("%Y%m%d%H%M%S")

# open page
browser.get('https://www.google.co.jp/')
sleep(wait_default)

# save screen shot image
diretory = '/app/screenShot/' + dtstr + '/'
if not os.path.exists(diretory):
  os.makedirs(diretory)
browser.save_screenshot(diretory + str(count_1) + '_' + browser.title + '.png')
count_1 += 1

# close
browser.close()
browser.quit()