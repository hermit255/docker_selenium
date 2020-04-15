#!/usr/local/bin/python3
from modules.driver import getChromeDriver, screenShot, getChromeHeadlessDriver
from modules.collector import collectInputs, exceptHiddenInput

import sys
from pprint import pprint
import traceback

url = 'https://google.com'
def test():
  try:
    driver = getChromeHeadlessDriver()
    driver.get(url)
    tags = collectInputs(driver)
    pprint(list(filter(exceptHiddenInput, tags)))
  except Exception as e:
    print(traceback.format_exc())
  finally:
    driver.close()
    driver.quit()
test()