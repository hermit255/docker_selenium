#!/usr/local/bin/python3
from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen
from modules.sites.testSite.pages import *
from modules.sites.sample.pages import *
from modules.analysis import getFormItems, createCsv, getAttrs
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import sys
from pprint import pprint
import traceback
import time

def test():
  pageTest()

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

def pageTest():
  driver = getChromeDriver()
  #driver = getChromeHeadlessDriver()
  try:
    page = GooglePage(driver)
    """
    driver = getChromeHeadlessDriver()
    page = GooglePage(driver)
    page = QuickRefSelectPage(driver)
    page = QuickRefRadioPage(driver)
    page = QuickRefCheckboxPage(driver)
    page = DocsApplyPage(driver)
    page = ApplyPage(driver)
    page = DocsApplyPage(driver)
    """

    page.test()
    time.sleep(3) # wait for page transition

    #fullScreen(driver)
    driver.set_window_size(1920, 4000)
    screenShot(driver, 'test')
    print('finished')
  except Exception as e:
    print(traceback.format_exc())
    driver.set_window_size(1920, 4000)
    screenShot(driver, 'failure')
  finally:
    pass
    #driver.close()
    #driver.quit()

def getForm():
  driver = getChromeDriver()
  #driver = getChromeHeadlessDriver()

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

test()