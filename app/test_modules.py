#!/usr/local/bin/python3
from modules.driver import getChromeDriver, screenShot, getChromeHeadlessDriver
from modules.analysis import collectInputs
from selenium.webdriver.remote.webelement import WebElement

import sys
from pprint import pprint
import traceback
import csv

#url = 'https://google.com'
url = 'https://shinronavi.com/omakase/select'
def test():
  try:
    driver = getChromeHeadlessDriver()
    driver.get(url)
    tags = collectInputs(driver)
    tags = list(filter(lambda tag: tag['type'] != 'hidden', tags))
    array = list(map(lambda tag: tag.values(), tags))
    with open('/app/storage/csv/sampleCsv.csv', 'w',  encoding='shift_jis') as f:
      writer = csv.writer(f)
      writer.writerow(tags[0])
      writer.writerows(array)
    pprint(tags)
  except Exception as e:
    print(traceback.format_exc())
  finally:
    driver.close()
    driver.quit()
test()