#!/usr/local/bin/python3
from modules.driver import getChromeDriver, screenShot, screenShotFull, getChromeHeadlessDriver
from modules.sites.testSite.pages import *
from modules.analysis import getFormItems, createCsv, getAttrs
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import sys
from pprint import pprint
import traceback
import time


url = 'https://google.com'
#url = 'https://shinronavi.com/omakase/select'
#url = 'https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver'
#url = 'http://www.htmq.com/html/select.shtml'

def test():
  driver = getChromeHeadlessDriver()
  page = XPage(driver)
  page.test()
  time.sleep(3) # wait for page transition
  screenShotFull(driver, 'test')
  """
  page = GooglePage(driver)
  page = QuickRefSelectPage(driver)
  page = QuickRefRadioPage(driver)
  page = QuickRefCheckboxPage(driver)
  page = XPage(driver)
  """
  print('finished')
  """
  locator = (By.XPATH, '//a')
  try:
    element = driver.find_element(*locator)
    attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    text = element.text

    pprint(text)
    pprint(attrs)

  except Exception as e:
    print(traceback.format_exc())
  finally:
  """
  driver.close()
  driver.quit()

def getForm():
  #driver = getChromeDriver()
  driver = getChromeHeadlessDriver()

  try:
    driver.get(url)

    tags = getFormItems(driver)
    tags = list(filter(lambda tag: tag['type'] != 'hidden', tags))
    createCsv(tags)
  except Exception as e:
    print(traceback.format_exc())
  finally:
    driver.close()
    driver.quit()

def screenShot():
  driver = getChromeHeadlessDriver()

  try:
    driver.get(url)
    subDir = url + '/'

    #screenShot(driver, title, subDir)
    screenShotFull(driver, driver.title, subDir)
  except Exception as e:
    print(traceback.format_exc())
  finally:
    driver.close()
    driver.quit()
test()