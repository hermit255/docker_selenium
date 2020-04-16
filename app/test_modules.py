#!/usr/local/bin/python3
from modules.driver import getChromeDriver, screenShot, screenShotFull, getChromeHeadlessDriver
from modules.analysis import getFormItems, createCsv
from selenium.webdriver.remote.webelement import WebElement

import sys
from pprint import pprint
import traceback
import time


url = 'https://google.com'
#url = 'https://shinronavi.com/omakase/select'
#url = 'https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver'
#url = 'http://www.htmq.com/html/select.shtml'

def test():
  driver = getChromeDriver()
  #driver = getChromeHeadlessDriver()

  try:
    driver.get(url)

    screenShot(driver)
    #screenShotFull(driver)

    tags = getFormItems(driver)
    tags = list(filter(lambda tag: tag['type'] != 'hidden', tags))
    createCsv(tags)
  except Exception as e:
    print(traceback.format_exc())
  finally:
    driver.close()
    driver.quit()
test()